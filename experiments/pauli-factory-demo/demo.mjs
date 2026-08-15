import { rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
await rm(path.join(root, 'runtime'), { recursive: true, force: true });
process.env.FACTORY_RUNTIME = path.join(root, 'runtime');
const { server } = await import('./src/server.mjs');

await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const { port } = server.address();
const base = `http://127.0.0.1:${port}`;
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function request(method, route, payload) {
  const res = await fetch(base + route, {
    method,
    headers: payload ? { 'content-type': 'application/json' } : undefined,
    body: payload ? JSON.stringify(payload) : undefined
  });
  return { status: res.status, body: await res.json() };
}

async function wait(jobId, terminal = ['COMPLETE', 'FAILED', 'BLOCKED', 'CANCELLED']) {
  for (let i = 0; i < 100; i++) {
    const result = await request('GET', `/jobs/${jobId}`);
    if (terminal.includes(result.body.state)) return result.body;
    await sleep(40);
  }
  throw new Error(`timeout waiting for ${jobId}`);
}

const health = await request('GET', '/healthz');
if (!health.body.ok) throw new Error('health failed');

const successful = await request('POST', '/jobs', {
  request_id: 'req_demo_success',
  repository: 'executiveusa/demo-repo',
  outcome: 'Change Hello to Welcome',
  constraints: ['no dependency changes'],
  proof: ['trusted tests', 'independent review'],
  budget: { runtime_minutes: 5, workers: 2, retries: 1, max_cost_usd: 1 },
  simulate_delay_ms: 100
});

const duplicate = await request('POST', '/jobs', {
  request_id: 'req_demo_success',
  repository: 'executiveusa/demo-repo',
  outcome: 'Change Hello to Welcome'
});
if (duplicate.body.job.job_id !== successful.body.job.job_id || !duplicate.body.idempotent_replay) throw new Error('idempotency failed');

const overlapping = await request('POST', '/jobs', {
  request_id: 'req_demo_overlap',
  repository: 'executiveusa/demo-repo',
  outcome: 'Concurrent conflicting change',
  budget: { max_cost_usd: 1 }
});

const failed = await request('POST', '/jobs', {
  request_id: 'req_demo_failure',
  repository: 'executiveusa/other-repo',
  outcome: 'Induce a test failure',
  simulate_failure: 'test',
  budget: { max_cost_usd: 1 }
});

const cancel = await request('POST', '/jobs', {
  request_id: 'req_demo_cancel',
  repository: 'executiveusa/cancel-repo',
  outcome: 'Long-running cancellable task',
  simulate_delay_ms: 350,
  budget: { max_cost_usd: 1 }
});
await sleep(80);
await request('POST', `/jobs/${cancel.body.job.job_id}/cancel`);

const [successJob, overlapJob, failedJob, cancelledJob] = await Promise.all([
  wait(successful.body.job.job_id),
  wait(overlapping.body.job.job_id),
  wait(failed.body.job.job_id),
  wait(cancel.body.job.job_id)
]);

const checks = {
  health: health.status === 200,
  successful_job_completed: successJob.state === 'COMPLETE',
  builder_reviewer_separated: successJob.evidence?.builder && successJob.evidence?.reviewer && successJob.evidence.builder !== successJob.evidence.reviewer,
  trusted_tests_passed: successJob.evidence?.tests?.passed === true,
  cleanup_proven: successJob.evidence?.cleanup?.worktree_removed === true,
  idempotency_proven: duplicate.body.idempotent_replay === true,
  overlap_blocked: overlapJob.state === 'BLOCKED',
  induced_failure_handled: failedJob.state === 'FAILED' && failedJob.failure === 'trusted tests failed',
  cancellation_handled: cancelledJob.state === 'CANCELLED',
  evidence_persisted: Boolean(successJob.evidence?.result_commit)
};

const pass = Object.values(checks).every(Boolean);
console.log(JSON.stringify({ pass, checks, jobs: {
  success: { id: successJob.job_id, state: successJob.state, evidence: successJob.evidence },
  overlap: { id: overlapJob.job_id, state: overlapJob.state, blocker: overlapJob.blocker },
  failure: { id: failedJob.job_id, state: failedJob.state, failure: failedJob.failure },
  cancelled: { id: cancelledJob.job_id, state: cancelledJob.state }
}}, null, 2));
server.close();
if (!pass) process.exit(1);
