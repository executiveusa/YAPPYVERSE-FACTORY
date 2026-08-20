#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawn } from 'node:child_process';

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
const visualQaPath = process.env.YAPPY_CLIPZ_VISUAL_QA_JSON || null;
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

function run(command, args, timeout = 60_000) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    const timer = setTimeout(() => {
      child.kill('SIGKILL');
      reject(new Error(`${command} timed out after ${timeout}ms`));
    }, timeout);
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('error', (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.on('close', (code) => {
      clearTimeout(timer);
      if (code !== 0) reject(new Error(`${command} exited ${code}: ${stderr.slice(-1000)}`));
      else resolve({ stdout, stderr });
    });
  });
}

async function downloadArtifact(url, destination, timeout = 120_000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(url, { signal: controller.signal, redirect: 'follow' });
    if (!response.ok) throw new Error(`artifact download -> ${response.status}`);
    const bytes = Buffer.from(await response.arrayBuffer());
    assert(bytes.length > 0, 'downloaded MP4 must be non-empty');
    await writeFile(destination, bytes);
    return bytes;
  } finally {
    clearTimeout(timer);
  }
}

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

async function inspectMp4(path) {
  const { stdout } = await run('ffprobe', [
    '-v', 'error',
    '-show_streams',
    '-show_format',
    '-of', 'json',
    path,
  ]);
  const probe = JSON.parse(stdout);
  const streams = Array.isArray(probe.streams) ? probe.streams : [];
  const video = streams.find((stream) => stream.codec_type === 'video');
  const audio = streams.find((stream) => stream.codec_type === 'audio');
  assert(video, 'ffprobe must find a video stream');
  assert(Number(video.width) === 1080, `ffprobe width must be 1080, got ${video.width}`);
  assert(Number(video.height) === 1920, `ffprobe height must be 1920, got ${video.height}`);
  const duration = Number(probe.format?.duration ?? video.duration);
  assert(Number.isFinite(duration) && duration > 0 && duration <= 30.5,
    `ffprobe duration must be >0 and <=30.5, got ${duration}`);

  const black = await run('ffmpeg', [
    '-hide_banner', '-nostats', '-i', path,
    '-vf', 'blackdetect=d=1:pix_th=0.98',
    '-an', '-f', 'null', '-',
  ], 120_000);
  const blackSegments = [...black.stderr.matchAll(/black_start:([0-9.]+) black_end:([0-9.]+) black_duration:([0-9.]+)/g)]
    .map((match) => ({ start: Number(match[1]), end: Number(match[2]), duration: Number(match[3]) }));
  const blackDuration = blackSegments.reduce((sum, segment) => sum + segment.duration, 0);
  assert(blackDuration < Math.max(1, duration * 0.9),
    `render appears black-frame-only or overwhelmingly black (${blackDuration.toFixed(2)}s of ${duration.toFixed(2)}s)`);

  return {
    width: Number(video.width),
    height: Number(video.height),
    duration_seconds: duration,
    video_codec: video.codec_name || null,
    audio_present: Boolean(audio),
    audio_codec: audio?.codec_name || null,
    black_duration_seconds: Number(blackDuration.toFixed(3)),
    black_segments: blackSegments,
  };
}

async function loadVisualQa() {
  assert(visualQaPath, 'YAPPY_CLIPZ_VISUAL_QA_JSON is required for V1 proof');
  const qa = JSON.parse(await readFile(visualQaPath, 'utf8'));
  assert(qa?.artifact_reviewed === true, 'visual QA must confirm the rendered artifact was reviewed');
  assert(qa?.captions_visible === true, 'visual QA must confirm captions are visibly present');
  assert(qa?.critical_findings_resolved === true, 'visual QA must confirm no unresolved critical findings');
  assert(typeof qa?.reviewer === 'string' && qa.reviewer.trim(), 'visual QA must identify an independent reviewer');
  return {
    artifact_reviewed: true,
    captions_visible: true,
    critical_findings_resolved: true,
    reviewer: qa.reviewer,
    evidence_ref: qa.evidence_ref || null,
  };
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
  artifact_verification: null,
  visual_qa: null,
  approval_required: true,
  finished_at: null,
};

let tempDir = null;
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
  assert(mp4.url, 'MP4 URL must be present');
  assert(mp4.checksum_sha256, 'MP4 checksum must be present');
  evidence.output_id = mp4.id;

  tempDir = await mkdtemp(join(tmpdir(), 'yappy-clipz-proof-'));
  const artifactPath = join(tempDir, 'output.mp4');
  const bytes = await downloadArtifact(mp4.url, artifactPath);
  const computedChecksum = sha256(bytes);
  assert(computedChecksum.toLowerCase() === String(mp4.checksum_sha256).toLowerCase(),
    `SHA-256 mismatch: service=${mp4.checksum_sha256} computed=${computedChecksum}`);

  const media = await inspectMp4(artifactPath);
  assert(mp4.width === media.width, `service width ${mp4.width} disagrees with ffprobe ${media.width}`);
  assert(mp4.height === media.height, `service height ${mp4.height} disagrees with ffprobe ${media.height}`);
  assert(Math.abs(Number(mp4.duration_seconds) - media.duration_seconds) <= 0.5,
    `service duration ${mp4.duration_seconds} disagrees with ffprobe ${media.duration_seconds}`);
  if (jobRequest.instructions.captions) evidence.visual_qa = await loadVisualQa();

  evidence.artifact_verification = {
    id: mp4.id,
    server_verified_claim: mp4.verified === true,
    checksum_sha256: computedChecksum,
    bytes: bytes.length,
    ...media,
    output_url_redacted: true,
  };
  evidence.finished_at = new Date().toISOString();

  console.log(JSON.stringify({
    result: 'READY_FOR_HUMAN_APPROVAL',
    next_action: `A human reviewer must inspect output ${mp4.id} and call POST /api/v1/projects/${project.id}/approve. Do not treat this run as production-approved until that separate approval is recorded and independently verified.`,
    evidence,
  }, null, 2));
} catch (error) {
  evidence.finished_at = new Date().toISOString();
  console.error(JSON.stringify({ result: 'FAIL', error: error.message, evidence }, null, 2));
  process.exitCode = 1;
} finally {
  if (tempDir) await rm(tempDir, { recursive: true, force: true });
}
