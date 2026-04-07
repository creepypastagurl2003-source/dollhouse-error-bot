import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from keep_alive import keep_alive
import os
import random
import logging
import asyncio

load_dotenv()

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
    await bot.tree.sync()
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


# ── Random movement detected — fires every 15–45 minutes ─────────────────────
@tasks.loop(minutes=30)
async def movement_task():
    """Send a random movement detected message to a channel in each guild."""
    # Small chance it fires (adds randomness to the interval feel)
    if random.random() > 0.6:
        return
    message = random.choice(MOVEMENT_MESSAGES)
    for guild in bot.guilds:
        # Pick the first text channel the bot can send in
        channel = next(
            (
                ch for ch in guild.text_channels
                if ch.permissions_for(guild.me).send_messages
            ),
            None,
        )
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
    """Send a rare glitch event to a random channel."""
    # Only fires 20% of the time — keeps it rare and spooky
    if random.random() > 0.2:
        return
    message = random.choice(GLITCH_EVENTS)
    for guild in bot.guilds:
        channel = next(
            (
                ch for ch in guild.text_channels
                if ch.permissions_for(guild.me).send_messages
            ),
            None,
        )
        if channel:
            try:
                await channel.send(message)
            except Exception:
                pass


@glitch_task.before_loop
async def before_glitch():
    await bot.wait_until_ready()
    await asyncio.sleep(random.randint(600, 1800))


# ── Entry point ───────────────────────────────────────────────────────────────
async def main():
    async with bot:
        await setup_hook_load()
        TOKEN = os.environ.get("BOT3_TOKEN")
        if not TOKEN:
            raise RuntimeError("BOT3_TOKEN environment variable is not set.")
        keep_alive()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
