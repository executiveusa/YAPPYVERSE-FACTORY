import { spawn } from 'node:child_process';

export async function runOrca(args, { binary = process.env.ORCA_BIN || 'orca', timeoutMs = 15000 } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(binary, args, { shell: false, env: process.env });
    let stdout = '';
    let stderr = '';
    const timer = setTimeout(() => {
      child.kill('SIGTERM');
      reject(new Error(`orca command timed out: ${args.join(' ')}`));
    }, timeoutMs);
    child.stdout.on('data', (d) => { stdout += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('error', (error) => { clearTimeout(timer); reject(error); });
    child.on('close', (code) => {
      clearTimeout(timer);
      if (code !== 0) return reject(new Error(`orca exited ${code}: ${stderr.trim().slice(0, 500)}`));
      resolve({ code, stdout, stderr });
    });
  });
}

export function parseJsonOutput(stdout, label) {
  try { return JSON.parse(stdout); }
  catch { throw new Error(`${label} did not return valid JSON`); }
}
