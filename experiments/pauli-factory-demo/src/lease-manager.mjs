export class LeaseManager {
  constructor() { this.leases = new Map(); }

  acquire(key, jobId, ttlMs = 30000) {
    const now = Date.now();
    const current = this.leases.get(key);
    if (current && current.expires_at > now && current.job_id !== jobId) return null;
    const lease = { key, job_id: jobId, acquired_at: now, heartbeat_at: now, expires_at: now + ttlMs };
    this.leases.set(key, lease);
    return lease;
  }

  heartbeat(key, jobId, ttlMs = 30000) {
    const lease = this.leases.get(key);
    if (!lease || lease.job_id !== jobId) return false;
    const now = Date.now();
    lease.heartbeat_at = now;
    lease.expires_at = now + ttlMs;
    return true;
  }

  release(key, jobId) {
    const lease = this.leases.get(key);
    if (lease?.job_id === jobId) this.leases.delete(key);
  }
}
