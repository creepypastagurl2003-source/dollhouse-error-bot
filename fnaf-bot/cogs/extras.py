import discord
from discord.ext import commands
from discord import app_commands
import random

# ── Glitch text substitutions ─────────────────────────────────────────────────
GLITCH_MAP = {
    "a": ["a", "4", "å", "à", "ā"],
    "e": ["e", "3", "ë", "ê", "€"],
    "i": ["i", "1", "í", "ï", "ì"],
    "o": ["o", "0", "ö", "ø", "ó"],
    "s": ["s", "5", "$", "§"],
    "t": ["t", "7", "+", "†"],
}
ZALGO_CHARS = [
    "\u0300", "\u0301", "\u0302", "\u0303", "\u0308",
    "\u0307", "\u0327", "\u0330", "\u0333", "\u0334",
]

# ── Haunt messages ─────────────────────────────────────────────────────────────
HAUNT_MESSAGES = [
    "is being watched. Don't look behind you.",
    "left the door open. That was a mistake.",
    "was seen on CAM 4B. They weren't alone.",
    "forgot to wind the music box. It's too late now.",
    "has been added to the roster. ♡",
    "is having a wonderful time at Freddy Fazbear's Pizza.",
    "didn't check the blind spot. They know now.",
    "will be joining us for the night shift.",
    "was found in the parts and service room. They seem… happy.",
    "is still here. We never left. ♡",
]

# ── Survive outcomes ────────────────────────────────────────────────────────────
SURVIVE_OUTCOMES = [
    (True, "You made it to 6AM. Barely. The sun has never looked so beautiful."),
    (True, "Survived. You don't know how. Neither do they."),
    (True, "The clock hit 6AM. You're safe. This time. ♡"),
    (True, "By some miracle, you're still here. Don't push your luck."),
    (False, "The power went out at 5:47AM. So close. ♡"),
    (False, "You checked the wrong camera at the wrong time. Game over."),
    (False, "Something was in the office. You just didn't know it yet."),
    (False, "You forgot to check Pirate Cove. Foxy remembers."),
    (False, "The music box stopped. You knew it would. ♡"),
]

# ── Camera sweep rooms ──────────────────────────────────────────────────────────
SWEEP_ROOMS = [
    ("CAM 1A — Show Stage", "🟢 Clear"),
    ("CAM 1B — Dining Area", "🟡 One chair is turned. Was it like that before?"),
    ("CAM 1C — Pirate Cove", "🔴 Curtain is open. Foxy is not there."),
    ("CAM 2A — West Hall", "🟡 Shadow at the end of the hall"),
    ("CAM 2B — West Hall Corner", "🔴 Camera offline"),
    ("CAM 3 — Supply Closet", "🟢 Clear"),
    ("CAM 4A — East Hall", "🟡 Movement — reclassified as shadow"),
    ("CAM 4B — East Hall Corner", "🔴 Something is standing at the corner"),
    ("CAM 5 — Backstage", "🟡 Spare suit is facing away from the wall"),
    ("CAM 6 — Kitchen", "🔴 Audio only. Singing detected."),
    ("CAM 7 — Restrooms", "🟢 Clear"),
    ("CAM 11 — Prize Corner", "🟢 Music box active ✅"),
]


def glitch_text(text: str) -> str:
    """Apply glitch/zalgo effect to text."""
    result = []
    for char in text:
        lower = char.lower()
        # Random character substitution
        if lower in GLITCH_MAP and random.random() < 0.4:
            char = random.choice(GLITCH_MAP[lower])
        result.append(char)
        # Add zalgo characters randomly
        if random.random() < 0.3:
            result.append(random.choice(ZALGO_CHARS))
    return "".join(result)


class Extras(commands.Cog):
    """Extra commands — glitch, haunt, survive, checkcams."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /glitch ────────────────────────────────────────────────────────────
    @app_commands.command(name="glitch", description="Send a distorted glitched transmission.")
    @app_commands.describe(message="Text to glitch (leave blank for a random transmission)")
    async def glitch(self, interaction: discord.Interaction, message: str = None):
        base_messages = [
            "I'm still here. I never left.",
            "It's me. Don't you remember?",
            "We are your friends. We are always your friends.",
            "The building is not safe. Leave. Or don't.",
            "Something followed you home. Check under the bed.",
            "Hello? Is anyone there? Hello hello hello hello",
            "PUT HIM BACK PUT HIM BACK PUT HIM BACK",
            "You can't hide from the cameras.",
        ]
        text = message if message else random.choice(base_messages)
        glitched = glitch_text(text)

        embed = discord.Embed(
            title="📡 G̷L̸I̷T̵C̶H̸ ̷T̸R̷A̴N̸S̷M̶I̴S̷S̸I̸O̷N̴",
            description=f"```{glitched}```",
            color=0x6c1a6c
        )
        embed.set_footer(text="Signal source: unknown ♡")
        await interaction.response.send_message(embed=embed)

    # ── /haunt ─────────────────────────────────────────────────────────────
    @app_commands.command(name="haunt", description="Send a creepy message targeting a user.")
    @app_commands.describe(user="The user to haunt")
    async def haunt(self, interaction: discord.Interaction, user: discord.Member):
        message = random.choice(HAUNT_MESSAGES)

        embed = discord.Embed(
            description=f"👁️ {user.mention} {message}",
            color=0x2b0a3d
        )
        embed.set_footer(text="We see everything. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /survive ────────────────────────────────────────────────────────────
    @app_commands.command(name="survive", description="Can you survive the night? Roll the dice.")
    async def survive(self, interaction: discord.Interaction):
        survived, outcome = random.choice(SURVIVE_OUTCOMES)

        if survived:
            embed = discord.Embed(
                title="✅ YOU SURVIVED",
                description=outcome,
                color=0x9b59b6
            )
        else:
            embed = discord.Embed(
                title="💀 GAME OVER",
                description=outcome,
                color=0xe74c3c
            )
        embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    # ── /checkcams ──────────────────────────────────────────────────────────
    @app_commands.command(name="checkcams", description="Simulate a full security camera sweep.")
    async def checkcams(self, interaction: discord.Interaction):
        # Pick 6–8 random cameras for the sweep
        sweep = random.sample(SWEEP_ROOMS, k=random.randint(6, 8))

        embed = discord.Embed(
            title="📷 FULL CAMERA SWEEP",
            description="*Cycling through all available feeds…*",
            color=0x2b0a3d
        )
        for cam, status in sweep:
            embed.add_field(name=cam, value=status, inline=False)

        # Determine overall threat
        reds = sum(1 for _, s in sweep if s.startswith("🔴"))
        if reds == 0:
            summary = "🟢 All clear. Enjoy it while it lasts."
        elif reds <= 2:
            summary = "🟡 Some anomalies detected. Stay alert."
        else:
            summary = "🔴 Multiple threats detected. Close the doors."

        embed.add_field(name="Overall Assessment", value=summary, inline=False)
        embed.set_footer(text="Sweep complete. Try not to think about the missing cameras. ♡")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Extras(bot))
