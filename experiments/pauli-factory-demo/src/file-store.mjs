import { mkdir, readFile, writeFile, readdir, rename } from 'node:fs/promises';
import path from 'node:path';

export class FileStore {
  constructor(root) {
    this.root = root;
    this.jobsDir = path.join(root, 'jobs');
    this.evidenceDir = path.join(root, 'evidence');
  }

  async init() {
    await mkdir(this.jobsDir, { recursive: true });
    await mkdir(this.evidenceDir, { recursive: true });
  }

  jobPath(jobId) { return path.join(this.jobsDir, `${jobId}.json`); }
  evidencePath(jobId) { return path.join(this.evidenceDir, `${jobId}.json`); }

  async putJob(job) {
    const target = this.jobPath(job.job_id);
    const temp = `${target}.${process.pid}.${Date.now()}.tmp`;
    await writeFile(temp, JSON.stringify(job, null, 2));
    await rename(temp, target);
  }

  async getJob(jobId) {
    try { return JSON.parse(await readFile(this.jobPath(jobId), 'utf8')); }
    catch (error) { if (error.code === 'ENOENT') return null; throw error; }
  }

  async findByRequestId(requestId) {
    const files = await readdir(this.jobsDir);
    for (const file of files) {
      if (!file.endsWith('.json')) continue;
      const job = JSON.parse(await readFile(path.join(this.jobsDir, file), 'utf8'));
      if (job.request_id === requestId) return job;
    }
    return null;
  }

  async putEvidence(jobId, evidence) {
    const target = this.evidencePath(jobId);
    const temp = `${target}.${process.pid}.${Date.now()}.tmp`;
    await writeFile(temp, JSON.stringify(evidence, null, 2));
    await rename(temp, target);
  }
}
