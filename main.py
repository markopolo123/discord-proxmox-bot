import proxmoxer
from pydantic import BaseModel
import discord
from discord.ext import commands
import os

# Define the configuration data for the ProxmoxVM object
config_data = {
    "hostname": f'{os.getenv("PVE_URL")}',
    "username": f'{os.getenv("PVE_USERNAME")}',
    "password": f'{os.getenv("PVE_PASSWORD")}',
    "node": f'{os.getenv("PVE_NODE")}',
    "vm_id": f'{os.getenv("VMID")}',
}


class ProxmoxVMConfig(BaseModel):
    hostname: str
    username: str
    password: str
    node: str
    vm_id: str


class ProxmoxVM:
    def __init__(self, config: ProxmoxVMConfig):
        self.proxmox = proxmoxer.ProxmoxAPI(
            config.hostname,
            user=config.username,
            password=config.password,
            verify_ssl=True,
        )
        self.vm = self.proxmox.nodes(config.node).qemu(config.vm_id)

    def start(self):
        self.vm.status.post("start")

    def shutdown(self):
        self.vm.status.post("shutdown")

    def status(self):
        status_dict = self.vm.status.current.get()
        return status_dict


DISCORD_TOKEN = f'{os.getenv("PVE_URL")}'
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def shutdown(ctx):
    # Create a ProxmoxVMConfig object from the configuration data
    config = ProxmoxVMConfig(**config_data)
    # Create a ProxmoxVM object from the configuration
    vm = ProxmoxVM(config)
    state = vm.status()
    if state["status"] == "stopped":
        message = "server already stopped"
        await ctx.channel.send(f"{message}")
    else:
        vm.shutdown()
        message = "server shutting down"
        await ctx.channel.send(f"{message}")


@bot.command()
async def start(ctx):
    # Create a ProxmoxVMConfig object from the configuration data
    config = ProxmoxVMConfig(**config_data)
    # Create a ProxmoxVM object from the configuration
    vm = ProxmoxVM(config)
    state = vm.status()
    if state["status"] == "running":
        message = "server already running"
        await ctx.channel.send(f"{message}")
    else:
        vm.start()
        message = "server started"
        await ctx.channel.send(f"{message}")


@bot.command()
async def status(ctx):
    # Create a ProxmoxVMConfig object from the configuration data
    config = ProxmoxVMConfig(**config_data)

    # Create a ProxmoxVM object from the configuration
    vm = ProxmoxVM(config)
    state = vm.status()
    await ctx.channel.send(f"🚀 Server Status: {state['status']}")


bot.run(DISCORD_TOKEN)
