import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Factory } from './factory.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const runtimeRoot = process.env.FACTORY_RUNTIME ?? path.resolve(__dirname, '../runtime');
export const factory = new Factory({ runtimeRoot });
await factory.init();

function json(res, status, body) {
  res.writeHead(status, { 'content-type': 'application/json' });
  res.end(JSON.stringify(body));
}

async function body(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return chunks.length ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : {};
}

export const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (req.method === 'GET' && url.pathname === '/healthz') return json(res, 200, { ok: true, service: 'pauli-factory-demo' });
    if (req.method === 'POST' && url.pathname === '/jobs') {
      const result = await factory.createJob(await body(req));
      return json(res, result.idempotent_replay ? 200 : 202, result);
    }
    const match = url.pathname.match(/^\/jobs\/([^/]+)(\/cancel)?$/);
    if (match && req.method === 'GET' && !match[2]) {
      const job = await factory.getJob(match[1]);
      return job ? json(res, 200, job) : json(res, 404, { error: 'not found' });
    }
    if (match && req.method === 'POST' && match[2] === '/cancel') {
      const job = await factory.cancelJob(match[1]);
      return job ? json(res, 202, job) : json(res, 404, { error: 'not found' });
    }
    return json(res, 404, { error: 'not found' });
  } catch (error) {
    return json(res, 400, { error: error.message });
  }
});

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT ?? 8787);
  server.listen(port, '127.0.0.1', () => console.log(`pauli-factory-demo listening on http://127.0.0.1:${port}`));
}
