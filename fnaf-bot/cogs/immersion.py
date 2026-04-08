import discord
from discord.ext import commands
from discord import app_commands
import random

# ── Door state (per guild, per user session) ───────────────────────────────────
_door_states: dict[int, dict[str, bool]] = {}  # guild_id → {left: bool, right: bool}

# ── Response pools ──────────────────────────────────────────────────────────────
LIGHT_RESULTS = [
    ("🟢 Clear", "Nothing in the hallway. The lights hold steady. Breathe.", 0x9b59b6),
    ("🟢 Clear", "Empty. The yellow wallpaper stares back at you. Nothing else.", 0x9b59b6),
    ("🟡 Movement", "Something shifted at the end of the hall. It stopped when the light hit it.", 0xe67e22),
    ("🟡 Shadow", "There's a shape in the corner. It might be the suit. It might not be.", 0xe67e22),
    ("🔴 WARNING", "It's right outside. You can see the suit. You can hear the breathing.", 0xe74c3c),
    ("🔴 LIGHTS OUT", "The bulb just blew. You are alone in the dark now. Close the door.", 0xe74c3c),
    ("🟡 Unknown", "You thought you saw something. When you looked again — nothing. Maybe.", 0xe67e22),
]

VENT_RESULTS = [
    ("🟢 All Clear", "Nothing in the vents. For now. Check again in a minute.", 0x9b59b6),
    ("🟢 All Clear", "Silent. Just the hum of the building. Peaceful, almost.", 0x9b59b6),
    ("🟡 Scratching", "Something is moving through the east vent. Slowly. Patiently.", 0xe67e22),
    ("🟡 Warmth", "The vent feels warmer than it should. Something passed through recently.", 0xe67e22),
    ("🔴 OCCUPIED", "There's something in the vent. Close it. Now.", 0xe74c3c),
    ("🔴 TOO LATE", "The vent cover is already off. Where did it go?", 0xe74c3c),
    ("🟡 Sound", "A soft humming from the vent shaft. It sounds almost like a lullaby.", 0xe67e22),
]

HIDE_RESULTS = [
    (True, "You hold your breath. The footsteps slow… then pass. They didn't find you. This time."),
    (True, "Pressed against the wall. Your heart is the loudest thing in the room. They moved on."),
    (True, "They walked right past. You could have touched it. Don't think about that."),
    (True, "The animatronic paused at the door. Then left. You don't know why. Be grateful."),
    (False, "You moved. Just for a second. It was enough. It always sees the ones who move."),
    (False, "You were found. Not because it searched hard — because it always knew where you were."),
    (False, "It sat perfectly still in the corner of the room while you hid. It was already there."),
    (False, "There is no hiding from something that can hear your heartbeat. ♡"),
]

EVENTS = [
    ("⚡ Power Surge", "The building drew more power than usual. Something activated in the back room.", 0xe67e22),
    ("📷 Camera Failure", f"CAM {random.randint(2, 8)} has gone offline. The feed shows only static — then nothing.", 0xe74c3c),
    ("👣 Movement Detected", "Motion sensors on the east corridor. Something is heading toward the office.", 0xe74c3c),
    ("🎵 Music Box", "The music box in the Prize Corner is slowing. Someone needs to wind it. Now.", 0xe67e22),
    ("🔒 Door Malfunction", "The left door mechanism is jammed. It won't close properly. Conserve power elsewhere.", 0xe67e22),
    ("🌑 Lights Out", "A section of the building just lost power. Something bypassed the breaker.", 0xe74c3c),
    ("📻 Transmission", "An audio recording plays from the back office. It's from 1987. No one should have that tape.", 0x9b59b6),
    ("🐾 Pirate Cove", "The curtain at Pirate Cove just moved. The sign now reads SORRY OUT OF ORDER. Be ready.", 0xe74c3c),
    ("🔧 System Override", "An unknown source accessed the security terminal. Commands were sent. Doors opened.", 0xe74c3c),
    ("🕯️ Quiet Period", "Everything is still. Cameras clear. Power stable. Enjoy it — it won't last. ♡", 0x9b59b6),
]

DANGER_LEVELS = [
    ("🟢 LOW", "Animatronics are on stage. Cameras functional. Power above 60%.\n*You probably won't die tonight.*", 0x2ecc71),
    ("🟡 MODERATE", "One unit has left its starting position. Power at 40–60%.\n*Stay attentive. Stay quiet.*", 0xe67e22),
    ("🟡 ELEVATED", "Multiple units active. Two cameras offline. Power dropping.\n*Close the doors. Check the vents.*", 0xe67e22),
    ("🔴 HIGH", "Animatronics in the hallways. Power below 30%. One camera feeds static.\n*Close everything. Pray.*", 0xe74c3c),
    ("💀 RUN", "Power at critical. Something is in the office. Cameras are down.\n*It's already too late. ♡*", 0x8b0000),
]

TIMES = [
    ("🕐 1 AM", "The first hour. They're just starting to move. Don't get comfortable."),
    ("🕑 2 AM", "Two hours in. Bonnie has left the stage. Check the left door."),
    ("🕒 3 AM", "The witching hour. They are most active right now. Don't blink."),
    ("🕓 4 AM", "Four hours. Power is running low. The end is in sight — or it isn't."),
    ("🕔 5 AM", "Almost there. One more hour. Don't celebrate yet. ♡"),
    ("🕠 5:30 AM", "Thirty minutes. Thirty agonizing minutes. Some nights, this is the hardest part."),
    ("🕕 6 AM", "The sun is rising. They've returned to the stage. You survived. For now."),
]


class Immersion(commands.Cog):
    """Immersion, roleplay, and random event commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_doors(self, guild_id: int) -> dict:
        if guild_id not in _door_states:
            _door_states[guild_id] = {"left": False, "right": False}
        return _door_states[guild_id]

    # ── /lockdoor ──────────────────────────────────────────────────────────
    @app_commands.command(name="lockdoor", description="Seal a security door. Costs power.")
    @app_commands.describe(side="Which door to lock: left or right")
    @app_commands.choices(side=[
        app_commands.Choice(name="Left", value="left"),
        app_commands.Choice(name="Right", value="right"),
    ])
    async def lockdoor(self, interaction: discord.Interaction, side: str = "left"):
        doors = self._get_doors(interaction.guild_id or 0)
        if doors[side]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"🔒 The **{side.upper()}** door is already sealed.",
                    color=0x2b0a3d
                ),
                ephemeral=True
            )
            return

        doors[side] = True
        drain = random.randint(7, 14)
        sound = random.choice([
            "A low mechanical groan as the door slides shut.",
            "Metal on metal. Heavy. Final.",
            "The door seals with a pressurized hiss.",
            "Something was at the door. Now it's not.",
        ])

        embed = discord.Embed(
            title=f"🔒 {side.upper()} DOOR — SEALED",
            description=f"*{sound}*\n\n⚡ Power drained: `{drain}%`",
            color=0x2b0a3d
        )
        embed.set_footer(text="Keep it closed. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /unlockdoor ────────────────────────────────────────────────────────
    @app_commands.command(name="unlockdoor", description="Reopen a security door.")
    @app_commands.describe(side="Which door to unlock: left or right")
    @app_commands.choices(side=[
        app_commands.Choice(name="Left", value="left"),
        app_commands.Choice(name="Right", value="right"),
    ])
    async def unlockdoor(self, interaction: discord.Interaction, side: str = "left"):
        doors = self._get_doors(interaction.guild_id or 0)
        if not doors[side]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"🔓 The **{side.upper()}** door is already open.",
                    color=0x2b0a3d
                ),
                ephemeral=True
            )
            return

        doors[side] = False
        comment = random.choice([
            "Are you sure that was wise?",
            "The hallway is quiet. Too quiet.",
            "Nothing came through. You got lucky.",
            "You hear something shuffle just outside. Then stop.",
        ])

        embed = discord.Embed(
            title=f"🔓 {side.upper()} DOOR — OPEN",
            description=f"*The door slides back. {comment}*",
            color=0x6c1a6c
        )
        embed.set_footer(text="Every second it's open costs you. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /lights ────────────────────────────────────────────────────────────
    @app_commands.command(name="lights", description="Flick on the hallway lights. Check for movement.")
    @app_commands.describe(side="Which hallway to check: left or right")
    @app_commands.choices(side=[
        app_commands.Choice(name="Left", value="Left"),
        app_commands.Choice(name="Right", value="Right"),
    ])
    async def lights(self, interaction: discord.Interaction, side: str = "Left"):
        status, message, color = random.choice(LIGHT_RESULTS)
        embed = discord.Embed(
            title=f"💡 {side.upper()} HALLWAY — LIGHTS ON",
            description=f"**{status}**\n\n{message}",
            color=color
        )
        embed.set_footer(text="Every flash of light costs power. Use it wisely. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /vent ──────────────────────────────────────────────────────────────
    @app_commands.command(name="vent", description="Check the ventilation system for activity.")
    async def vent(self, interaction: discord.Interaction):
        status, message, color = random.choice(VENT_RESULTS)
        embed = discord.Embed(
            title="🌀 VENT INSPECTION",
            description=f"**{status}**\n\n{message}",
            color=color
        )
        embed.set_footer(text="They love the vents. Small spaces. Quiet places. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /hide ──────────────────────────────────────────────────────────────
    @app_commands.command(name="hide", description="Attempt to hide from an animatronic.")
    async def hide(self, interaction: discord.Interaction):
        success, outcome = random.choice(HIDE_RESULTS)
        title = "✅ HIDDEN — You were not found." if success else "💀 FOUND — They always find you."
        color = 0x9b59b6 if success else 0xe74c3c
        embed = discord.Embed(title=title, description=outcome, color=color)
        embed.set_footer(text=f"Attempted by {interaction.user.display_name} ♡")
        await interaction.response.send_message(embed=embed)

    # ── /event ─────────────────────────────────────────────────────────────
    @app_commands.command(name="event", description="Trigger a random security event.")
    async def event(self, interaction: discord.Interaction):
        title, description, color = random.choice(EVENTS)
        embed = discord.Embed(title=f"⚠️ EVENT — {title}", description=description, color=color)
        embed.set_footer(text="Log this. Keep a record. It matters later. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /danger ────────────────────────────────────────────────────────────
    @app_commands.command(name="danger", description="Check the current danger level in the building.")
    async def danger(self, interaction: discord.Interaction):
        level, description, color = random.choice(DANGER_LEVELS)
        embed = discord.Embed(
            title=f"📊 THREAT ASSESSMENT — {level}",
            description=description,
            color=color
        )
        embed.set_footer(text="Levels are re-evaluated every minute. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /timer ─────────────────────────────────────────────────────────────
    @app_commands.command(name="timer", description="Check the current time in your night shift.")
    async def timer(self, interaction: discord.Interaction):
        time_str, note = random.choice(TIMES)
        embed = discord.Embed(
            title=f"🕰️ CURRENT TIME — {time_str}",
            description=note,
            color=0x2b0a3d
        )
        embed.set_footer(text="6AM can't come soon enough. ♡")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Immersion(bot))
