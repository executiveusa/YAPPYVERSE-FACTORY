import crypto from 'node:crypto';
import { FileStore } from './file-store.mjs';
import { LeaseManager } from './lease-manager.mjs';
import { MockOrcaAdapter } from './mock-orca-adapter.mjs';

const TERMINAL = new Set(['COMPLETE', 'FAILED', 'BLOCKED', 'CANCELLED']);
const now = () => new Date().toISOString();

export class Factory {
  constructor({ runtimeRoot, adapter = new MockOrcaAdapter() }) {
    this.store = new FileStore(runtimeRoot);
    this.leases = new LeaseManager();
    this.adapter = adapter;
    this.controllers = new Map();
  }

  async init() { await this.store.init(); }

  validate(input) {
    for (const field of ['request_id', 'repository', 'outcome']) {
      if (!input[field] || typeof input[field] !== 'string') throw new Error(`missing ${field}`);
    }
    const budget = input.budget ?? {};
    if ((budget.max_cost_usd ?? 5) <= 0) throw new Error('budget.max_cost_usd must be > 0');
    if ((budget.runtime_minutes ?? 30) <= 0) throw new Error('budget.runtime_minutes must be > 0');
  }

  async createJob(input) {
    this.validate(input);
    const existing = await this.store.findByRequestId(input.request_id);
    if (existing) return { job: existing, idempotent_replay: true };

    const jobId = `job_${crypto.randomUUID()}`;
    const job = {
      job_id: jobId,
      request_id: input.request_id,
      repository: input.repository,
      outcome: input.outcome,
      constraints: input.constraints ?? [],
      proof: input.proof ?? [],
      budget: { runtime_minutes: 30, max_cost_usd: 5, workers: 2, retries: 1, ...(input.budget ?? {}) },
      simulate_failure: input.simulate_failure ?? null,
      simulate_delay_ms: input.simulate_delay_ms ?? 80,
      state: 'RECEIVED',
      created_at: now(),
      updated_at: now(),
      history: [{ state: 'RECEIVED', at: now() }],
      cancel_requested: false
    };
    await this.store.putJob(job);
    const controller = new AbortController();
    this.controllers.set(jobId, controller);
    setImmediate(() => this.run(jobId, controller.signal).catch(() => {}));
    return { job, idempotent_replay: false };
  }

  async transition(job, state, extra = {}) {
    job.state = state;
    job.updated_at = now();
    job.history.push({ state, at: job.updated_at });
    Object.assign(job, extra);
    await this.store.putJob(job);
  }

  async cancelled(job, signal) {
    const fresh = await this.store.getJob(job.job_id);
    return signal.aborted || fresh?.cancel_requested;
  }

  async checkpoint(job, signal) {
    if (await this.cancelled(job, signal)) {
      await this.transition(job, 'CANCELLED', { finished_at: now() });
      return false;
    }
    return true;
  }

  async run(jobId, signal) {
    const job = await this.store.getJob(jobId);
    if (!job || TERMINAL.has(job.state)) return;
    const lockKey = `repo:${job.repository}:global`;
    const lease = this.leases.acquire(lockKey, jobId);
    if (!lease) {
      await this.transition(job, 'BLOCKED', { blocker: 'repo lease held by another job', finished_at: now() });
      return;
    }

    const started = Date.now();
    let workspace;
    try {
      await this.transition(job, 'VALIDATING');
      if (!(await this.checkpoint(job, signal))) return;

      if ((job.budget.max_cost_usd ?? 0) < 0.01) {
        await this.transition(job, 'BLOCKED', { blocker: 'budget exhausted', finished_at: now() });
        return;
      }

      await this.transition(job, 'ORIENTING');
      if (!(await this.checkpoint(job, signal))) return;

      await this.transition(job, 'PREPARING_WORKSPACE');
      workspace = await this.adapter.prepare(job);
      if (!(await this.checkpoint(job, signal))) return;

      await this.transition(job, 'BUILDING', { workspace });
      const build = await this.adapter.build(job, workspace);
      if (!(await this.checkpoint(job, signal))) return;

      await this.transition(job, 'TESTING');
      const tests = await this.adapter.test(job, build);
      if (!tests.passed) {
        const cleanup = await this.adapter.cleanup(job, workspace);
        const evidence = this.evidence(job, build, tests, null, cleanup, started);
        await this.store.putEvidence(jobId, evidence);
        await this.transition(job, 'FAILED', { failure: 'trusted tests failed', evidence, finished_at: now() });
        return;
      }
      if (!(await this.checkpoint(job, signal))) return;

      await this.transition(job, 'REVIEWING');
      const review = await this.adapter.review(job, build, tests);
      const cleanup = await this.adapter.cleanup(job, workspace);
      const evidence = this.evidence(job, build, tests, review, cleanup, started);
      await this.store.putEvidence(jobId, evidence);

      if (review.verdict !== 'PASS') {
        await this.transition(job, 'FAILED', { failure: 'independent review failed', evidence, finished_at: now() });
        return;
      }
      await this.transition(job, 'COMPLETE', { evidence, finished_at: now() });
    } catch (error) {
      if (workspace) {
        try { await this.adapter.cleanup(job, workspace); } catch {}
      }
      await this.transition(job, signal.aborted ? 'CANCELLED' : 'FAILED', { failure: error.message, finished_at: now() });
    } finally {
      this.leases.release(lockKey, jobId);
      this.controllers.delete(jobId);
    }
  }

  evidence(job, build, tests, review, cleanup, started) {
    return {
      job_id: job.job_id,
      request_id: job.request_id,
      repository: job.repository,
      base_commit: build?.workspace?.base_commit ?? null,
      result_commit: build?.result_commit ?? null,
      branch: build?.workspace?.branch ?? null,
      worktree: build?.workspace?.worktree ?? null,
      builder: build?.worker ?? null,
      reviewer: review?.reviewer ?? null,
      changed_files: build?.changed_files ?? [],
      diff_summary: build?.diff_summary ?? {},
      tests,
      review,
      cost: { estimated_usd: 0.02, budget_usd: job.budget.max_cost_usd },
      started_at: new Date(started).toISOString(),
      completed_at: now(),
      cleanup
    };
  }

  async getJob(jobId) { return this.store.getJob(jobId); }

  async cancelJob(jobId) {
    const job = await this.store.getJob(jobId);
    if (!job) return null;
    if (TERMINAL.has(job.state)) return job;
    job.cancel_requested = true;
    job.updated_at = now();
    await this.store.putJob(job);
    this.controllers.get(jobId)?.abort();
    return job;
  }
}
