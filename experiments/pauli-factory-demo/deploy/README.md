# VPS deployment notes

This is a template, not permission to overwrite an existing Hostinger/Coolify topology.

Before use:
1. inventory the VPS and existing Coolify/systemd services;
2. create a dedicated `pauli-factory` user if compatible with the host;
3. place code at `/opt/pauli-factory` and writable state at `/var/lib/pauli-factory`;
4. run `node src/capability-discovery.mjs` as the runtime user;
5. bind the real Orca adapter only after the snapshot proves exact command semantics;
6. keep the HTTP service private or behind Hermes authentication; do not expose an unrestricted executor publicly.
