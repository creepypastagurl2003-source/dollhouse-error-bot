import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from keep_alive import keep_alive
import os
import random
import logging
import asyncio
import json

load_dotenv()

# ── Channel config (persists which channel gets ambient messages per guild) ────
_CONFIG_FILE = "channel_config.json"

def _load_config() -> dict:
    try:
        with open(_CONFIG_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_config(cfg: dict):
    with open(_CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

_channel_config: dict = _load_config()  # {str(guild_id): channel_id}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("fnaf-bot")

# ── Bot setup ─────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ── Random movement detected messages ─────────────────────────────────────────
MOVEMENT_MESSAGES = [
    "👁️ *Movement detected on CAM 2A…*",
    "⚠️ *Something just left the Show Stage.*",
    "📷 *Camera 4B has gone offline.*",
    "🔇 *The music box has slowed down. Someone should wind it.*",
    "👣 *Footsteps in the east hallway. The floor is old. You can hear everything.*",
    "🪟 *The window in the office just fogged up. From the inside.*",
    "📻 *Static on all frequencies. Then breathing. Then silence.*",
    "⚡ *Power fluctuation detected. Not from the generator.*",
    "🌙 *It's 3AM. They're the most active now.*",
    "🐾 *CAM 1C — Pirate Cove: The curtain is open. Foxy is gone.*",
    "👁️ *Something is staring at CAM 7. It knows you can see it.*",
    "🔒 *A door just opened. You didn't open it.*",
]

# ── Rare glitch event messages ─────────────────────────────────────────────────
GLITCH_EVENTS = [
    "```\nE̷R̸R̷O̸R̷:̸ ̷C̸A̷M̸E̷R̸A̷ ̸F̷E̸E̷D̷ ̸C̸O̸R̸R̸U̷P̸T̷E̸D̷\nR̷e̸s̷t̸o̷r̸i̷n̷g̸.̷.̷.̸ R̸e̷s̸t̷o̸r̷i̸n̷g̸.̷.̷.̸\nI̷ ̷s̸e̷e̷ ̸y̷o̷u̷.̸\n```",
    "```\nSYSTEM OVERRIDE DETECTED\nSource: Unknown\nMessage: IT'S ME\n```",
    "```\nA̴L̴E̴R̴T̴:̴ ̴A̴N̴I̴M̴A̴T̴R̴O̴N̴I̴C̴ ̴I̴N̴ ̴O̴F̴F̴I̴C̴E̴\n[This event has been removed from the logs]\n```",
    "```\nPOWER: 0%\nDOORS: OPEN\nCAMERAS: OFFLINE\nGOOD LUCK ♡\n```",
    "```\nHello? Is anyone there?\nHello? Hello?\nhello hello hello hello hello hello\n```",
]


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} ({bot.user.id})")
    # Sync slash commands to each guild instantly (guild sync is immediate,
    # unlike global sync which can take up to an hour to propagate)
    # Copy global commands into each guild's local store first
    for guild in bot.guilds:
        bot.tree.copy_global_to(guild=guild)
    # Clear the global store and push empty to Discord (removes old global duplicates)
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    # Now push guild-specific commands to each guild
    for guild in bot.guilds:
        try:
            await bot.tree.sync(guild=guild)
            logger.info(f"Commands synced to guild: {guild.name} ({guild.id})")
        except Exception as e:
            logger.warning(f"Failed to sync to guild {guild.id}: {e}")
    logger.info("Slash commands synced.")
    # Start background tasks
    movement_task.start()
    glitch_task.start()
    logger.info("Background tasks started.")


async def setup_hook_load():
    """Load all cogs before the bot connects."""
    cogs = [
        "cogs.core", "cogs.fnaf", "cogs.characters", "cogs.extras",
        "cogs.immersion", "cogs.gameplay", "cogs.cutecreepy",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"Loaded cog: {cog}")
        except Exception as e:
            logger.error(f"Failed to load cog {cog}: {e}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_ambient_channel(guild: discord.Guild) -> discord.TextChannel | None:
    """Return the configured channel for a guild, or fall back to first available."""
    cid = _channel_config.get(str(guild.id))
    if cid:
        ch = guild.get_channel(int(cid))
        if ch and ch.permissions_for(guild.me).send_messages:
            return ch
    # Fallback: first channel the bot can write in
    return next(
        (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
        None,
    )


# ── Random movement detected — fires every 15–45 minutes ─────────────────────
@tasks.loop(minutes=30)
async def movement_task():
    """Send a random movement detected message to a channel in each guild."""
    if random.random() > 0.6:
        return
    message = random.choice(MOVEMENT_MESSAGES)
    for guild in bot.guilds:
        channel = _get_ambient_channel(guild)
        if channel:
            try:
                await channel.send(message)
            except Exception:
                pass


@movement_task.before_loop
async def before_movement():
    await bot.wait_until_ready()
    # Random initial delay so it doesn't fire immediately
    await asyncio.sleep(random.randint(300, 900))


# ── Rare glitch event — fires every 60–120 minutes ────────────────────────────
@tasks.loop(minutes=90)
async def glitch_task():
    """Send a rare glitch event to the configured channel."""
    if random.random() > 0.2:
        return
    message = random.choice(GLITCH_EVENTS)
    for guild in bot.guilds:
        channel = _get_ambient_channel(guild)
        if channel:
            try:
                await channel.send(message)
            except Exception:
                pass


# ── Channel config commands ────────────────────────────────────────────────────

@bot.tree.command(name="setchannel", description="Set the channel for ambient FNAF messages.")
@app_commands.describe(channel="The channel to send ambient messages to (defaults to current channel).")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.guild_only()
async def setchannel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    target = channel or interaction.channel
    _channel_config[str(interaction.guild.id)] = target.id
    _save_config(_channel_config)
    await interaction.response.send_message(
        f"📷 *Camera feeds and alerts redirected to {target.mention}. "
        f"They'll know where to look now.* 👁️",
        ephemeral=True,
    )

@setchannel.error
async def setchannel_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("🔒 *You need `Manage Channels` to do that.*", ephemeral=True)


@bot.tree.command(name="clearchannel", description="Reset ambient channel — falls back to first available.")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.guild_only()
async def clearchannel(interaction: discord.Interaction):
    _channel_config.pop(str(interaction.guild.id), None)
    _save_config(_channel_config)
    await interaction.response.send_message(
        "📷 *Channel override cleared. I'll find my own way in. 🌙*",
        ephemeral=True,
    )


@bot.tree.command(name="testambient", description="Send a test ambient message to the configured channel now.")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.guild_only()
async def testambient(interaction: discord.Interaction):
    channel = _get_ambient_channel(interaction.guild)
    if channel:
        message = random.choice(MOVEMENT_MESSAGES)
        await channel.send(message)
        await interaction.response.send_message(f"📷 *Sent to {channel.mention}. 👁️*", ephemeral=True)
    else:
        await interaction.response.send_message("📷 *No channel available.*", ephemeral=True)


@glitch_task.before_loop
async def before_glitch():
    await bot.wait_until_ready()
    await asyncio.sleep(random.randint(600, 1800))


# ── Entry point ───────────────────────────────────────────────────────────────
async def main():
    # On Replit (not Render), just run the keep-alive server so the workflow
    # stays healthy without competing with Render for the same bot token.
    if not os.environ.get("RENDER"):
        logger.info("Not running on Render — starting keep-alive only. Discord connection skipped.")
        keep_alive()
        await asyncio.sleep(float("inf"))
        return

    async with bot:
        await setup_hook_load()
        TOKEN = os.environ.get("BOT3_TOKEN")
        if not TOKEN:
            raise RuntimeError("BOT3_TOKEN environment variable is not set.")
        keep_alive()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
