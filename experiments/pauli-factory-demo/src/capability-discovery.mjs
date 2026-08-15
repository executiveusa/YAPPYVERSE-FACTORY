import { writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { runOrca, parseJsonOutput } from './orca-command.mjs';

const commands = [
  ['status', '--json'],
  ['skills', 'list', '--json'],
  ['skills', 'get', 'orca-cli', '--json'],
  ['skills', 'get', 'orchestration', '--full', '--json']
];

function redact(value) {
  const sensitive = /token|secret|password|private.?key|api.?key|credential/i;
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, val]) => [key, sensitive.test(key) ? '[REDACTED]' : redact(val)]));
  }
  return value;
}

export async function discoverCapabilities({ outDir = process.env.FACTORY_RUNTIME || './runtime' } = {}) {
  const snapshot = { captured_at: new Date().toISOString(), commands: {} };
  for (const args of commands) {
    const label = `orca ${args.join(' ')}`;
    const result = await runOrca(args, { timeoutMs: 30000 });
    snapshot.commands[label] = redact(parseJsonOutput(result.stdout, label));
  }
  await mkdir(outDir, { recursive: true });
  const outPath = path.join(outDir, 'orca-capabilities.json');
  await writeFile(outPath, JSON.stringify(snapshot, null, 2));
  return { snapshot, outPath };
}

if (process.argv[1]?.endsWith('capability-discovery.mjs')) {
  discoverCapabilities().then(({ outPath }) => console.log(JSON.stringify({ ok: true, outPath }))).catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message }));
    process.exit(1);
  });
}
