import { discoverCapabilities } from './capability-discovery.mjs';

export class RealOrcaAdapter {
  constructor() {
    this.capabilities = null;
  }

  async preflight() {
    const { snapshot } = await discoverCapabilities();
    this.capabilities = snapshot;
    return snapshot;
  }

  async prepare() {
    throw new Error('REAL_ORCA_ADAPTER_NOT_BOUND: inspect runtime capability snapshot and bind exact version-matched worktree command before enabling live jobs');
  }

  async build() {
    throw new Error('REAL_ORCA_ADAPTER_NOT_BOUND');
  }

  async test() {
    throw new Error('REAL_ORCA_ADAPTER_NOT_BOUND');
  }

  async review() {
    throw new Error('REAL_ORCA_ADAPTER_NOT_BOUND');
  }

  async cleanup() {
    throw new Error('REAL_ORCA_ADAPTER_NOT_BOUND');
  }
}
