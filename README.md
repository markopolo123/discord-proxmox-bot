## Discord Bot for controlling a Proxmox VM

Uses the python libraries discord.py and proxmoxer to start, shutdown and show running status of a Proxmox QEMU VM in discord

## Install

```bash
poetry install
```

## Running

You'll need to have configured a bot in discord and invited it to your server.

### Env variables

```bash
export VMID="111"
export PVE_PASSWORD="12345"
export PVE_USERNAME="user@pam"
export PVE_NODE="pvenodenamehere"
export PVE_URL="pve.url.here"
export DISCORD_TOKEN="12345"
```

### Starting the bot

```bash
poetry run python main.py
```

### Using the Bot

| Command   | Purpose                  |
|-----------|--------------------------|
| $start    | starts vm                |
| $shutdown | shutdown the vm          |
| $status   | running status of the VM |
