const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export class MockOrcaAdapter {
  async prepare(job) {
    await sleep(job.simulate_delay_ms ?? 80);
    return {
      worktree: `orca-wt-${job.job_id}`,
      branch: `factory/${job.job_id}`,
      base_commit: 'demo-base-sha'
    };
  }

  async build(job, workspace) {
    await sleep(job.simulate_delay_ms ?? 80);
    return {
      worker: 'opencode-builder',
      result_commit: `demo-result-${job.job_id.slice(-6)}`,
      changed_files: ['demo/target.txt'],
      diff_summary: { additions: 1, deletions: 1 },
      workspace
    };
  }

  async test(job) {
    await sleep(job.simulate_delay_ms ?? 80);
    if (job.simulate_failure === 'test') {
      return { passed: false, suite: 'trusted-demo-suite', output: 'induced test failure' };
    }
    return { passed: true, suite: 'trusted-demo-suite', output: '1 passed' };
  }

  async review(job, build, test) {
    await sleep(job.simulate_delay_ms ?? 80);
    if (job.simulate_failure === 'review') {
      return { reviewer: 'independent-reviewer', verdict: 'FAIL', reason: 'induced reviewer rejection' };
    }
    return {
      reviewer: 'independent-reviewer',
      verdict: test.passed ? 'PASS' : 'FAIL',
      reason: test.passed ? 'bounded change matches contract' : 'tests failed'
    };
  }

  async cleanup(job, workspace) {
    await sleep(20);
    return { worktree_removed: true, workspace: workspace.worktree };
  }
}
