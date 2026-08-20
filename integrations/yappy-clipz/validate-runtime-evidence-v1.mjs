#!/usr/bin/env node

import { readFile } from 'node:fs/promises';

const [evidencePath = 'yappy-clipz-v1-evidence.json', manifestPath = new URL('./runtime-acceptance-v1.json', import.meta.url)] = process.argv.slice(2);

function assert(condition, message) {
  if (!condition) throw new Error(`ACCEPTANCE FAILED: ${message}`);
}

const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
const evidence = JSON.parse(await readFile(evidencePath, 'utf8'));

for (const key of manifest.required_evidence) {
  assert(evidence[key] !== undefined && evidence[key] !== null, `missing required evidence: ${key}`);
}

assert(typeof evidence.montage_commit_sha === 'string' && /^[a-f0-9]{40}$/i.test(evidence.montage_commit_sha), 'montage_commit_sha must be a full SHA');
assert(typeof evidence.preview_deployment_id === 'string' && evidence.preview_deployment_id.trim(), 'preview_deployment_id required');
assert(typeof evidence.project_id === 'string' && evidence.project_id.trim(), 'project_id required');
assert(typeof evidence.asset_id === 'string' && evidence.asset_id.trim(), 'asset_id required');
assert(typeof evidence.job_id === 'string' && evidence.job_id.trim(), 'job_id required');
assert(typeof evidence.output_id === 'string' && evidence.output_id.trim(), 'output_id required');

assert(evidence.idempotency_proof?.same_job_id === true, 'idempotency proof must show same job id');
assert(Array.isArray(evidence.job_state_trace) && evidence.job_state_trace.length > 0, 'job_state_trace must be non-empty');
const statuses = evidence.job_state_trace.map((entry) => entry.status);
assert(statuses.includes('ready') || statuses.includes('approved'), 'job trace must reach ready or approved');
assert(!statuses.some((status, index) => ['failed', 'rejected', 'cancelled'].includes(status) && index < statuses.length - 1), 'terminal failure cannot transition onward');

assert(typeof evidence.output_sha256 === 'string' && /^[a-f0-9]{64}$/i.test(evidence.output_sha256), 'output_sha256 must be valid');
assert(Number(evidence.ffprobe_summary?.width) === manifest.mp4_gate.width, `width must be ${manifest.mp4_gate.width}`);
assert(Number(evidence.ffprobe_summary?.height) === manifest.mp4_gate.height, `height must be ${manifest.mp4_gate.height}`);
assert(Number(evidence.ffprobe_summary?.duration_seconds) > manifest.mp4_gate.min_duration_seconds_exclusive, 'duration must be > 0');
assert(Number(evidence.ffprobe_summary?.duration_seconds) <= manifest.mp4_gate.max_duration_seconds, `duration must be <= ${manifest.mp4_gate.max_duration_seconds}`);
assert(evidence.ffprobe_summary?.video_stream_present === true, 'video stream required');
if (evidence.ffprobe_summary?.audio_expected === true) assert(evidence.ffprobe_summary?.audio_stream_present === true, 'expected audio stream missing');

assert(evidence.black_frame_analysis?.passed === true, 'black-frame analysis must pass');
assert(evidence.visual_qa?.artifact_reviewed === true, 'visual QA must review artifact');
assert(evidence.visual_qa?.critical_findings_resolved === true, 'critical visual findings must be resolved');
assert(typeof evidence.visual_qa?.reviewer === 'string' && evidence.visual_qa.reviewer.trim(), 'visual QA reviewer identity required');

assert(evidence.human_approval?.approved === true, 'separate human approval required');
assert(typeof evidence.human_approval?.approved_by === 'string' && evidence.human_approval.approved_by.trim(), 'human approval identity required');
assert(typeof evidence.human_approval?.approved_at === 'string' && evidence.human_approval.approved_at.trim(), 'human approval timestamp required');
assert(evidence.human_approval?.output_id === evidence.output_id, 'approval must refer to the verified output');

assert(evidence.ci_green === true, 'CI/review must be green');
assert(typeof evidence.rollback === 'string' && evidence.rollback.trim(), 'rollback evidence required');
assert(evidence.publish_side_effect === false, 'V1 proof must have no publishing side effect');
assert(evidence.capcut_used === false, 'CapCut must not be required for V1');

console.log(JSON.stringify({
  result: 'YAPPY_CLIPZ_V1_ACCEPTED',
  service: manifest.service,
  recipe: manifest.recipe,
  project_id: evidence.project_id,
  job_id: evidence.job_id,
  output_id: evidence.output_id,
  approved_by: evidence.human_approval.approved_by
}, null, 2));
