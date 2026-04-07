import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

# ── Camera feeds ────────────────────────────────────────────────────────────
CAMERA_FEEDS = [
    ("CAM 1A — Show Stage", "Everything looks normal on stage… for now.", False),
    ("CAM 1B — Dining Area", "The tables are empty. One chair is slightly turned.", False),
    ("CAM 1C — Pirate Cove", "The curtain is closed. *Do not open the curtain.*", False),
    ("CAM 2A — West Hall", "The hallway is dark. Something glints in the shadows.", True),
    ("CAM 2B — West Hall Corner", "Static. Then nothing. Then static again.", True),
    ("CAM 3 — Supply Closet", "A pair of eyes blink in the dark. Feed lost.", True),
    ("CAM 4A — East Hall", "Movement detected. Camera stable.", False),
    ("CAM 4B — East Hall Corner", "S̷o̷m̷e̷t̷h̷i̷n̷g̷ i̷s̷ s̷t̷a̷n̷d̷i̷n̷g̷ t̷h̷e̷r̷e̷.", True),
    ("CAM 5 — Backstage", "Spare parts. Empty suits. One suit is facing the wrong way.", True),
    ("CAM 6 — Kitchen", "Audio only. The sound of… singing? The pots are moving.", True),
    ("CAM 7 — Restrooms", "The light flickers. You see your own reflection. Then you don't.", True),
    ("CAM 11 — Prize Corner", "The music box is still playing. Everything is fine. ♡", False),
]

# ── Animatronic status messages ──────────────────────────────────────────────
STATUS_MESSAGES = [
    ("Freddy Fazbear", "At the Show Stage. Watching.", "🟢"),
    ("Bonnie", "Left the stage. Location unknown.", "🔴"),
    ("Chica", "Moving through the kitchen. Do not look.", "🟡"),
    ("Foxy", "Curtain slightly open. Monitoring advised.", "🟡"),
    ("Golden Freddy", "Not detected. That's worse.", "⚫"),
    ("Mangle", "Signal lost. Last seen: ceiling vent.", "🔴"),
    ("The Puppet", "In the box. Music box: ACTIVE. ✅", "🟢"),
    ("Springtrap", "Movement in Hallway B. Seal the vent.", "🔴"),
    ("Nightmare Fredbear", "He is at the end of the bed. Do not open your eyes.", "⚫"),
    ("Circus Baby", "She says everything is fine. It is not fine.", "🟡"),
    ("Vanny", "Untracked. She does not want to be found.", "🔴"),
    ("Sun / Moon", "Lights: ON. Attendant is cheerful. Keep the lights on.", "🟢"),
]

# ── FNAF quotes ─────────────────────────────────────────────────────────────
QUOTES = [
    "\"They used to hold birthday parties here, you know.\"",
    "\"It's me.\"",
    "\"I always come back.\"",
    "\"You can't hide from me forever.\"",
    "\"The building does not discriminate. It is always watching.\"",
    "\"Hello, hello? Uh… I wanted to record a message for you.\"",
    "\"They're not dangerous. Probably.\"",
    "\"There's no one left to fix them anymore.\"",
    "\"You survived the night. Curious.\"",
    "\"The music box must be wound. Always.\"",
    "\"I'm still here.\"",
    "\"We are still your friends. ♡\"",
    "\"Do you remember me?\"",
    "\"Everything is fine. I promise.\"",
    "\"Come find me. I'll be waiting.\"",
    "\"Put him back. Put him back or it won't stop.\"",
    "\"I… I don't want to hurt you.\"",
    "\"Something is wrong with the suits.\"",
    "\"Remnant lingers in the walls. Can you feel it?\"",
    "\"Stay until 6AM. You'll be okay. Probably.\"",
]

# ── Night descriptions ───────────────────────────────────────────────────────
NIGHTS = {
    1: {
        "title": "🌙 NIGHT 1 — Your First Shift",
        "desc": "The animatronics are still in their resting state. Almost. Bonnie has left the stage.",
        "difficulty": "Easy",
        "color": 0x9b59b6,
        "tip": "Keep an eye on the left door. You have plenty of power tonight.",
    },
    2: {
        "title": "🌙 NIGHT 2 — It Gets Worse",
        "desc": "Multiple animatronics are active now. Foxy is peeking through the curtain. Stay alert.",
        "difficulty": "Moderate",
        "color": 0x8e44ad,
        "tip": "Wind the music box. Check Pirate Cove. Listen for sounds in the kitchen.",
    },
    3: {
        "title": "🌙 NIGHT 3 — Something is Different",
        "desc": "The cameras glitch more frequently. An animatronic is outside your office. You can feel it.",
        "difficulty": "Hard",
        "color": 0x6c3483,
        "tip": "Conserve power. Do not leave the doors closed for too long. Check the hallways.",
    },
    4: {
        "title": "🌙 NIGHT 4 — The Golden Hours",
        "desc": "Power reserves are critically low. The cameras are unreliable. They are everywhere now.",
        "difficulty": "Very Hard",
        "color": 0x4a235a,
        "tip": "Prioritize Foxy. Freddy moves when you stop watching. The end of the hall has something in it.",
    },
    5: {
        "title": "🌙 NIGHT 5 — THE FINAL SHIFT",
        "desc": "The phones have stopped ringing. The building hums with something old and hungry. Survive until 6AM.",
        "difficulty": "🔴 CRITICAL",
        "color": 0x1a0a2e,
        "tip": "Everything is active. Every sound is a warning. Good luck. You'll need it.",
    },
}


class FNAF(commands.Cog):
    """FNAF-themed commands — cameras, power, status, night, jumpscare, quote."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Per-guild power level (starts at 100)
        self.power: dict[int, int] = {}
        # Per-guild current night
        self.current_night: dict[int, int] = {}

    def get_power(self, guild_id: int) -> int:
        return self.power.get(guild_id, 100)

    def drain_power(self, guild_id: int, amount: int = 5):
        current = self.get_power(guild_id)
        self.power[guild_id] = max(0, current - amount)

    # ── /cameras ──────────────────────────────────────────────────────────
    @app_commands.command(name="cameras", description="Check the security camera feeds.")
    async def cameras(self, interaction: discord.Interaction):
        self.drain_power(interaction.guild_id, 3)
        cam_name, desc, creepy = random.choice(CAMERA_FEEDS)

        color = 0x6c1a6c if creepy else 0x2b0a3d
        warning = "⚠️ **MOVEMENT DETECTED**\n" if creepy else ""

        embed = discord.Embed(
            title=f"📷 {cam_name}",
            description=f"{warning}{desc}",
            color=color
        )
        embed.set_footer(text=f"Power remaining: {self.get_power(interaction.guild_id)}% | Camera feed may not be accurate.")
        await interaction.response.send_message(embed=embed)

    # ── /power ────────────────────────────────────────────────────────────
    @app_commands.command(name="power", description="Check the current power level.")
    async def power_cmd(self, interaction: discord.Interaction):
        pct = self.get_power(interaction.guild_id)
        filled = int(pct / 10)
        bar = "█" * filled + "░" * (10 - filled)

        if pct > 60:
            status = "Stable. You have time."
            color = 0x9b59b6
        elif pct > 30:
            status = "⚠️ Power draining. Be careful."
            color = 0xe67e22
        elif pct > 10:
            status = "🔴 CRITICAL — Use doors sparingly!"
            color = 0xe74c3c
        else:
            status = "💀 **POWER OUT** — He's coming."
            color = 0x1a0a0a

        embed = discord.Embed(
            title="⚡ POWER LEVEL",
            description=f"`[{bar}]` **{pct}%**\n\n{status}",
            color=color
        )
        embed.set_footer(text="When the power goes out, so do you.")
        await interaction.response.send_message(embed=embed)

    # ── /status ────────────────────────────────────────────────────────────
    @app_commands.command(name="status", description="Get a current animatronic status report.")
    async def status(self, interaction: discord.Interaction):
        # Pick 3–5 random animatronics to report on
        sample = random.sample(STATUS_MESSAGES, k=random.randint(3, 5))

        embed = discord.Embed(
            title="🔍 ANIMATRONIC STATUS REPORT",
            description="*Report generated. Accuracy not guaranteed.*",
            color=0x2b0a3d
        )
        for name, loc, indicator in sample:
            embed.add_field(name=f"{indicator} {name}", value=loc, inline=False)

        embed.set_footer(text="Locations may have changed since this report was generated.")
        await interaction.response.send_message(embed=embed)

    # ── /night ────────────────────────────────────────────────────────────
    @app_commands.command(name="night", description="Begin your night shift. Night 1 through 5.")
    @app_commands.describe(night="Which night to start (1–5)")
    async def night(self, interaction: discord.Interaction, night: int = None):
        if night is None:
            # Progress from current night or start at 1
            current = self.current_night.get(interaction.guild_id, 0)
            night = min(current + 1, 5)

        night = max(1, min(5, night))
        self.current_night[interaction.guild_id] = night
        # Reset power each new night
        self.power[interaction.guild_id] = 100

        data = NIGHTS[night]
        embed = discord.Embed(
            title=data["title"],
            description=data["desc"],
            color=data["color"]
        )
        embed.add_field(name="Difficulty", value=data["difficulty"], inline=True)
        embed.add_field(name="Power", value="100% ⚡", inline=True)
        embed.add_field(name="💡 Tip", value=data["tip"], inline=False)
        embed.set_footer(text="6AM feels very far away right now.")
        await interaction.response.send_message(embed=embed)

        # Dramatic follow-up message after a few seconds
        await asyncio.sleep(4)
        follow_ups = [
            "*Something moved in the hallway.*",
            "⚠️ Movement detected — CAM 2A.",
            "*The music box has slowed down.*",
            "*A door creaks somewhere in the building.*",
            "*You hear breathing. It isn't yours.*",
        ]
        await interaction.followup.send(random.choice(follow_ups))

    # ── /jumpscare ─────────────────────────────────────────────────────────
    @app_commands.command(name="jumpscare", description="Something is watching. Do you dare?")
    async def jumpscare(self, interaction: discord.Interaction):
        self.drain_power(interaction.guild_id, 5)
        roll = random.random()

        if roll < 0.35:
            # Safe
            messages = [
                "…nothing. Just the shadows playing tricks.",
                "You checked. Everything is fine. *For now.*",
                "The hallway is empty. You think.",
                "Safe. This time. ♡",
                "You held your breath for nothing. Almost nothing.",
            ]
            embed = discord.Embed(description=random.choice(messages), color=0x2b0a3d)
        elif roll < 0.75:
            # Creepy but not fatal
            messages = [
                "S̷o̷m̷e̷t̷h̷i̷n̷g̷ w̷a̷s̷ t̷h̷e̷r̷e̷. It moved away.",
                "The camera glitched. When it came back — the hallway was empty. It wasn't before.",
                "You heard it. You know you heard it.",
                "M̵o̵v̵e̵m̵e̵n̵t̵ ̵d̵e̵t̵e̵c̵t̵e̵d̵. ̵S̵o̵u̵r̵c̵e̵:̵ ̵u̵n̵k̵n̵o̵w̵n̵.",
                "It was right outside the door. You can still hear it breathing.",
            ]
            embed = discord.Embed(description=f"⚠️ {random.choice(messages)}", color=0x6c1a6c)
        else:
            # Jumpscare
            self.power[interaction.guild_id] = 0
            messages = [
                "# 😱 IT'S IN THE OFFICE\n*GAME OVER*\n\nYou didn't check the blind spot.",
                "# 💀 THEY GOT YOU\n\nThe last thing you heard was a laugh.",
                "# 😱 JUMPSCARE\n\nThe power went out. Something stepped through the dark.",
                "# ☠️ YOU ARE THE BITE\n\n*Please remember to smile.*",
            ]
            embed = discord.Embed(description=random.choice(messages), color=0xe74c3c)

        await interaction.response.send_message(embed=embed)

    # ── /quote ─────────────────────────────────────────────────────────────
    @app_commands.command(name="quote", description="Receive a transmission from the dark.")
    async def quote(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📻 Incoming Transmission…",
            description=f"*{random.choice(QUOTES)}*",
            color=0x2b0a3d
        )
        embed.set_footer(text="— Source unknown")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(FNAF(bot))
