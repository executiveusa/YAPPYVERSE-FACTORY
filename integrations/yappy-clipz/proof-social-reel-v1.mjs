#!/usr/bin/env node

const required = ['YAPPY_CLIPZ_BASE_URL', 'YAPPY_CLIPZ_TOKEN', 'YAPPY_CLIPZ_SOURCE_URL'];
for (const key of required) {
  if (!process.env[key]) throw new Error(`Missing required env var: ${key}`);
}

const baseUrl = process.env.YAPPY_CLIPZ_BASE_URL.replace(/\/$/, '');
const token = process.env.YAPPY_CLIPZ_TOKEN;
const sourceUrl = process.env.YAPPY_CLIPZ_SOURCE_URL;
const tenantId = process.env.YAPPY_CLIPZ_TENANT_ID || `proof-${Date.now()}`;
const timeoutMs = Number(process.env.YAPPY_CLIPZ_TIMEOUT_MS || 10 * 60_000);
const pollMs = Number(process.env.YAPPY_CLIPZ_POLL_MS || 2_000);
const startedAt = new Date().toISOString();

async function request(path, init = {}, timeout = 30_000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(`${baseUrl}${path}`, {
      ...init,
      signal: controller.signal,
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${token}`,
        ...(init.headers || {}),
      },
    });
    const text = await response.text();
    const body = text ? JSON.parse(text) : null;
    if (!response.ok) {
      throw new Error(`${init.method || 'GET'} ${path} -> ${response.status}: ${text.slice(0, 500)}`);
    }
    return { status: response.status, body };
  } finally {
    clearTimeout(timer);
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(`PROOF FAILED: ${message}`);
}

async function pollJob(jobId) {
  const deadline = Date.now() + timeoutMs;
  const trace = [];
  while (Date.now() < deadline) {
    const remaining = Math.max(1_000, deadline - Date.now());
    const { body: job } = await request(`/api/v1/jobs/${encodeURIComponent(jobId)}`, {}, Math.min(30_000, remaining));
    trace.push({ at: new Date().toISOString(), status: job.status, progress: job.progress ?? null });
    if (['ready', 'approved'].includes(job.status)) return { job, trace };
    if (['failed', 'rejected', 'cancelled'].includes(job.status)) {
      throw new Error(`Job ${job.id} ended in ${job.status}: ${job.error?.message || 'no error detail'}`);
    }
    await new Promise((resolve) => setTimeout(resolve, Math.min(pollMs, Math.max(0, deadline - Date.now()))));
  }
  throw new Error(`Job ${jobId} timed out after ${timeoutMs}ms`);
}

const evidence = {
  started_at: startedAt,
  tenant_id: tenantId,
  base_url: baseUrl,
  project_id: null,
  asset_id: null,
  job_id: null,
  output_id: null,
  job_trace: [],
  output: null,
  approval: null,
  finished_at: null,
};

try {
  const { status: projectStatus, body: project } = await request('/api/v1/projects', {
    method: 'POST',
    body: JSON.stringify({ tenant_id: tenantId, name: `social-reel-v1-proof-${Date.now()}` }),
  });
  assert(projectStatus === 201, 'project creation must return 201');
  assert(project?.id, 'project must return id');
  evidence.project_id = project.id;

  const { status: assetStatus, body: asset } = await request(`/api/v1/projects/${encodeURIComponent(project.id)}/assets`, {
    method: 'POST',
    body: JSON.stringify({ tenant_id: tenantId, kind: 'video', source_url: sourceUrl, filename: 'proof-source.mp4' }),
  });
  assert(assetStatus === 201, 'asset registration must return 201');
  assert(asset?.id, 'asset must return id');
  evidence.asset_id = asset.id;

  const idempotencyKey = `social-reel-v1-${tenantId}-${asset.id}`;
  const jobRequest = {
    tenant_id: tenantId,
    recipe: 'social_reel_v1',
    source_asset_ids: [asset.id],
    instructions: {
      duration_seconds: 30,
      width: 1080,
      height: 1920,
      captions: true,
      hook: true,
      cta: true,
      platform: 'instagram',
    },
    outputs: ['mp4'],
    idempotency_key: idempotencyKey,
  };

  const first = await request(`/api/v1/projects/${encodeURIComponent(project.id)}/jobs`, {
    method: 'POST',
    body: JSON.stringify(jobRequest),
  });
  assert(first.status === 202, 'job creation must return 202');
  assert(first.body?.id, 'job must return id');
  evidence.job_id = first.body.id;

  const second = await request(`/api/v1/projects/${encodeURIComponent(project.id)}/jobs`, {
    method: 'POST',
    body: JSON.stringify(jobRequest),
  });
  assert(second.body?.id === first.body.id, 'idempotent retry must return the same job id');

  const { job, trace } = await pollJob(first.body.id);
  evidence.job_trace = trace;
  assert(['ready', 'approved'].includes(job.status), 'job must reach ready or approved');

  const { body: outputResponse } = await request(`/api/v1/projects/${encodeURIComponent(project.id)}/outputs`);
  const mp4 = outputResponse?.outputs?.find((output) => output.kind === 'mp4' && output.status === 'ready');
  assert(mp4, 'ready MP4 output must exist');
  assert(mp4.verified === true, 'MP4 output must be verified');
  assert(mp4.width === 1080, `MP4 width must be 1080, got ${mp4.width}`);
  assert(mp4.height === 1920, `MP4 height must be 1920, got ${mp4.height}`);
  assert(typeof mp4.duration_seconds === 'number' && mp4.duration_seconds > 0 && mp4.duration_seconds <= 30.5,
    `MP4 duration must be >0 and <=30.5, got ${mp4.duration_seconds}`);
  assert(mp4.checksum_sha256, 'MP4 checksum must be present');
  assert(mp4.url, 'MP4 URL must be present');
  evidence.output_id = mp4.id;
  evidence.output = {
    id: mp4.id,
    verified: mp4.verified,
    width: mp4.width,
    height: mp4.height,
    duration_seconds: mp4.duration_seconds,
    checksum_sha256: mp4.checksum_sha256,
    url: mp4.url,
  };

  const { status: approvalStatus, body: approved } = await request(`/api/v1/projects/${encodeURIComponent(project.id)}/approve`, {
    method: 'POST',
    body: JSON.stringify({ approved_by: 'external-proof-harness', output_id: mp4.id }),
  });
  assert(approvalStatus === 200, 'approval must return 200');
  assert(approved?.status === 'approved', 'project must be approved after explicit approval');
  evidence.approval = { status: approved.status, approved_by: 'external-proof-harness' };
  evidence.finished_at = new Date().toISOString();

  console.log(JSON.stringify({ result: 'PASS', evidence }, null, 2));
} catch (error) {
  evidence.finished_at = new Date().toISOString();
  console.error(JSON.stringify({ result: 'FAIL', error: error.message, evidence }, null, 2));
  process.exitCode = 1;
}
