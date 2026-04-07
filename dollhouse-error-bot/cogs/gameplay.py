import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import datetime

# ── Shift difficulty settings ──────────────────────────────────────────────────
NIGHTS = {
    1: ("Night 1 — Tutorial", "They barely move. You have time to learn. Use it.", 0x9b59b6, "Low"),
    2: ("Night 2 — They're Awake", "Bonnie is very active. Don't ignore Chica either.", 0x9b59b6, "Low–Medium"),
    3: ("Night 3 — All Active", "Everyone is moving now. Foxy runs if you ignore Pirate Cove.", 0xe67e22, "Medium"),
    4: ("Night 4 — Panic Mode", "Almost no warning before they reach the office.", 0xe67e22, "Medium–High"),
    5: ("Night 5 — Final Night", "Golden Freddy is a possibility tonight. Don't stare.", 0xe74c3c, "High"),
    6: ("Night 6 — Extra Credit", "The manager called this optional. He lied.", 0xe74c3c, "Extreme"),
    7: ("Night 7 — Custom Night", "Max difficulty. They never stop. You chose this. ♡", 0x8b0000, "MAXIMUM"),
}

SHIFT_RESULTS = [
    (True, "6AM — The building falls quiet. Another night survived. Don't think about tomorrow."),
    (True, "The power held. Barely. You watched the clock tick to 6 and didn't breathe until it did."),
    (True, "They were close. Multiple times. But you made it. ♡"),
    (True, "Survived. The morning crew found you at your desk, pale and silent. They didn't ask questions."),
    (False, "The power hit 0% at 5:47AM. The doors opened. You knew what was next."),
    (False, "You checked the wrong camera. Just once. That's all it took."),
    (False, "Freddy laughed from the darkness. Then the screen went dark."),
    (False, "Something was in the office long before you realized it. ♡"),
    (False, "The music box ran out. You heard it stop. You already knew."),
]

POWER_COMPONENTS = [
    ("💡 Lighting System", lambda: f"{random.randint(8, 25)}%"),
    ("🚪 Door Mechanisms", lambda: f"{random.randint(15, 40)}%"),
    ("📷 Camera Array", lambda: f"{random.randint(10, 20)}%"),
    ("🔊 Audio System", lambda: f"{random.randint(3, 10)}%"),
    ("🌡️ Ventilation", lambda: f"{random.randint(5, 15)}%"),
]

SURVIVAL_FACTORS = [
    ("Power Management", ["Poor ❌", "Adequate ⚠️", "Excellent ✅"]),
    ("Camera Monitoring", ["Neglected ❌", "Intermittent ⚠️", "Diligent ✅"]),
    ("Door Usage", ["Overused ❌", "Balanced ⚠️", "Optimal ✅"]),
    ("Music Box", ["Forgotten ❌", "Nearly missed ⚠️", "Maintained ✅"]),
    ("Composure", ["Panicking ❌", "Stressed ⚠️", "Steady ✅"]),
]

LOG_TYPES = [
    "Unusual audio detected in Dining Area",
    "Camera 4B reported offline — possible animatronic interference",
    "Foxy observed at halfway point in west corridor",
    "Music box wound at 02:34 AM — no further issues",
    "Power fluctuation lasting 3 seconds — cause unknown",
    "Golden Freddy poster observed in office — source unknown",
    "Door held closed for 4 minutes — power impact severe",
    "All cameras functional — no movement on show stage",
    "Movement detected in Parts & Service — suit repositioned",
    "Ballora heard singing in corridor — visual not confirmed",
]

INCIDENTS = [
    ("Animatronic Left Starting Position", "Unit observed moving from show stage at 01:12 AM. Camera tracking lost at 02:40 AM.", "High"),
    ("Camera Feed Disrupted", "Feed for CAM 2B shows corrupted signal for approximately 8 minutes.", "Medium"),
    ("Power System Anomaly", "Unexplained power draw of 14% detected. Source not identified.", "High"),
    ("Audio Disturbance", "Unscheduled audio playback detected in West Hall. No source found.", "Medium"),
    ("Door Override Attempt", "Left security door received an override command from an unregistered source.", "Critical"),
    ("Staff Member Missing", "Night guard did not check in for end-of-shift. Office is empty. Coffee is still warm.", "Critical"),
    ("Music Box Failure", "Prize Corner music box ceased operation at 03:22 AM. Intervention required.", "High"),
    ("Suit Misalignment", "Endoskeleton detected in incorrect storage suit. Tag reads: 'Completed'.", "Critical"),
]

SCAN_RESULTS = [
    "All systems nominal. Threat level: MINIMAL. Proceed with caution.",
    "Biometric scan complete. Subject identified. Status: OBSERVED.",
    "Signal detected. Origin: Parts & Service. Threat level: ELEVATED.",
    "User record found. Last seen: Friday. Status: Still here. ♡",
    "Facial recognition match: 97.3%. Adding to the roster. Welcome.",
    "No anomalies found. But we're still watching. Always. ♡",
    "Scan interrupted. Unknown entity interfered. Rebooting…",
    "ALERT: Subject matches a missing persons report from 1987.",
]


class Gameplay(commands.Cog):
    """Gameplay, system, and utility commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._shifts: dict[int, int] = {}  # user_id → night number

    # ── /startshift ────────────────────────────────────────────────────────
    @app_commands.command(name="startshift", description="Begin your night shift. Good luck.")
    @app_commands.describe(night="Night number (1–7). Default is random.")
    async def startshift(self, interaction: discord.Interaction, night: int = None):
        n = max(1, min(7, night)) if night else random.randint(1, 5)
        self._shifts[interaction.user.id] = n
        label, briefing, color, threat = NIGHTS[n]

        embed = discord.Embed(
            title=f"📋 SHIFT STARTED — {label}",
            description=(
                f"*The clock reads 12:00 AM. The building is quiet.*\n\n"
                f"{briefing}"
            ),
            color=color
        )
        embed.add_field(name="⚠️ Threat Level", value=threat, inline=True)
        embed.add_field(name="⚡ Starting Power", value="100%", inline=True)
        embed.add_field(name="🕐 Current Time", value="12 AM", inline=True)
        embed.set_footer(text="Use /endshift when you reach 6AM — or don't. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /endshift ──────────────────────────────────────────────────────────
    @app_commands.command(name="endshift", description="End your current night shift.")
    async def endshift(self, interaction: discord.Interaction):
        night = self._shifts.pop(interaction.user.id, random.randint(1, 5))
        survived, outcome = random.choice(SHIFT_RESULTS)

        if survived:
            embed = discord.Embed(
                title="☀️ NIGHT COMPLETE — YOU SURVIVED",
                description=outcome,
                color=0x9b59b6
            )
            embed.add_field(name="🌙 Night Completed", value=str(night), inline=True)
            embed.add_field(name="💰 Paycheck", value=f"${random.randint(90, 120)}.00", inline=True)
            embed.add_field(name="📝 Review", value=random.choice(["Good work.", "Adequate performance.", "You're still alive. That's enough."]), inline=False)
        else:
            embed = discord.Embed(
                title="💀 SHIFT ENDED — YOU DID NOT MAKE IT",
                description=outcome,
                color=0xe74c3c
            )
            embed.add_field(name="⏱️ Time of Incident", value=f"{random.randint(1, 5)}:{random.choice(['12', '27', '43', '58'])} AM", inline=True)
            embed.add_field(name="📝 Cause", value="See incident report.", inline=True)

        embed.set_footer(text=f"Guard: {interaction.user.display_name} ♡")
        await interaction.response.send_message(embed=embed)

    # ── /checkpower ────────────────────────────────────────────────────────
    @app_commands.command(name="checkpower", description="View a detailed power consumption report.")
    async def checkpower(self, interaction: discord.Interaction):
        total = random.randint(8, 97)
        color = 0x2ecc71 if total > 60 else (0xe67e22 if total > 25 else 0xe74c3c)

        embed = discord.Embed(
            title="⚡ POWER MANAGEMENT REPORT",
            description=f"**Total Remaining: `{total}%`**\n*{'All systems operational.' if total > 60 else 'Power is dangerously low. Reduce usage.' if total <= 25 else 'Power running low. Conserve where possible.'}*",
            color=color
        )
        for component, fn in POWER_COMPONENTS:
            embed.add_field(name=component, value=fn(), inline=True)

        if total <= 25:
            embed.add_field(
                name="⚠️ CRITICAL WARNING",
                value="At current consumption rate, power will fail in under 1 hour. Close all non-essential systems.",
                inline=False
            )
        embed.set_footer(text="Power is your lifeline. Guard it. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /survivalrate ──────────────────────────────────────────────────────
    @app_commands.command(name="survivalrate", description="Calculate your odds of surviving the night.")
    async def survivalrate(self, interaction: discord.Interaction):
        scores = [random.randint(0, 2) for _ in SURVIVAL_FACTORS]
        rate = int((sum(scores) / (len(scores) * 2)) * 100)
        color = 0x2ecc71 if rate >= 70 else (0xe67e22 if rate >= 40 else 0xe74c3c)

        embed = discord.Embed(
            title="📊 SURVIVAL PROBABILITY ANALYSIS",
            description=f"**Survival Rate: `{rate}%`**",
            color=color
        )
        for (factor, options), score in zip(SURVIVAL_FACTORS, scores):
            embed.add_field(name=factor, value=options[score], inline=True)

        verdict = (
            "You might actually make it. Don't get cocky." if rate >= 70 else
            "Possible, but unlikely. Pray for good RNG." if rate >= 40 else
            "You are not going to make it. Sorry. ♡"
        )
        embed.add_field(name="📝 Assessment", value=verdict, inline=False)
        embed.set_footer(text=f"Calculated for {interaction.user.display_name} ♡")
        await interaction.response.send_message(embed=embed)

    # ── /log ───────────────────────────────────────────────────────────────
    @app_commands.command(name="log", description="Create an official night log entry.")
    @app_commands.describe(note="Your observation (leave blank for a random entry)")
    async def log(self, interaction: discord.Interaction, note: str = None):
        now = datetime.utcnow()
        timestamp = now.strftime("%m/%d/%Y — %I:%M %p UTC")
        entry = note if note else random.choice(LOG_TYPES)

        embed = discord.Embed(
            title="📓 NIGHT LOG — NEW ENTRY",
            description=f"*Filed by {interaction.user.display_name}*",
            color=0x2b0a3d
        )
        embed.add_field(name="🕐 Timestamp", value=timestamp, inline=False)
        embed.add_field(name="📝 Observation", value=entry, inline=False)
        embed.add_field(name="🔖 Status", value="Logged. Management has been notified. Probably.", inline=False)
        embed.set_footer(text="All logs are reviewed. Eventually. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /report ────────────────────────────────────────────────────────────
    @app_commands.command(name="report", description="Generate a formal incident report.")
    async def report(self, interaction: discord.Interaction):
        incident, details, severity = random.choice(INCIDENTS)
        color = {"Critical": 0x8b0000, "High": 0xe74c3c, "Medium": 0xe67e22}.get(severity, 0x9b59b6)
        report_id = f"FFP-{random.randint(1000, 9999)}"
        now = datetime.utcnow().strftime("%m/%d/%Y")

        embed = discord.Embed(
            title=f"📋 INCIDENT REPORT — {report_id}",
            color=color
        )
        embed.add_field(name="📅 Date", value=now, inline=True)
        embed.add_field(name="🔎 Severity", value=severity, inline=True)
        embed.add_field(name="👤 Reporting Officer", value=interaction.user.display_name, inline=True)
        embed.add_field(name="📌 Incident Type", value=incident, inline=False)
        embed.add_field(name="📝 Details", value=details, inline=False)
        embed.add_field(name="📬 Status", value="Under review. Management is aware. The building is still open.", inline=False)
        embed.set_footer(text="Freddy Fazbear's Pizza — Safety is our #1 priority. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /scan ──────────────────────────────────────────────────────────────
    @app_commands.command(name="scan", description="Run a security scan on a user or the system.")
    @app_commands.describe(target="User to scan (leave blank to scan the system)")
    async def scan(self, interaction: discord.Interaction, target: discord.Member = None):
        await interaction.response.defer()
        result = random.choice(SCAN_RESULTS)

        embed = discord.Embed(
            title="🔍 SECURITY SCAN — RESULTS",
            color=0x2b0a3d
        )

        if target:
            embed.description = f"*Scanning {target.mention}…*"
            embed.add_field(name="🪪 Subject", value=target.display_name, inline=True)
            embed.add_field(name="🆔 ID", value=f"`{target.id}`", inline=True)
            embed.add_field(name="📡 Result", value=result, inline=False)
            embed.set_thumbnail(url=target.display_avatar.url)
        else:
            embed.description = "*Scanning building systems…*"
            embed.add_field(name="🏢 Location", value="Freddy Fazbear's Pizza — Main Office", inline=False)
            embed.add_field(name="📡 Result", value=result, inline=False)
            embed.add_field(name="📷 Cameras", value=f"{random.randint(5, 11)}/12 online", inline=True)
            embed.add_field(name="⚡ Power", value=f"{random.randint(20, 99)}%", inline=True)

        embed.set_footer(text="Scan complete. We are always scanning. ♡")
        await interaction.followup.send(embed=embed)

    # ── /error ─────────────────────────────────────────────────────────────
    @app_commands.command(name="error", description="Trigger a system failure message.")
    async def error_cmd(self, interaction: discord.Interaction):
        errors = [
            ("FATAL ERROR", "```\nFATAL ERROR — PROCESS 0x4F\nStack overflow detected in audio subsystem.\nMemory dump: IT'S ME IT'S ME IT'S ME\nRestarting… Restarting… .\n```"),
            ("SYSTEM CRASH", "```\n[CRITICAL] Animatronic override signal received.\n[CRITICAL] Access level: GOD\n[CRITICAL] Shutting down cameras… doors… lights…\nHello.\n```"),
            ("CORRUPTED LOG", "```\nERROR: Log file corrupted.\nLast entry: 'something is in the'\nRemaining data: ██████████████\nFile size: 0 bytes\n```"),
            ("CONNECTION LOST", "```\nSECURITY FEED DISCONNECTED\nAttempting reconnect… failed\nAttempting reconnect… failed\nAttempting reconnect… it answered.\n```"),
            ("DATABASE ERROR", "```\nEmployee record not found.\nLast paycheck: unclaimed.\nWorkplace status: ██████████\nHR note: Do not open the suit.\n```"),
        ]
        title, description = random.choice(errors)
        embed = discord.Embed(title=f"❌ {title}", description=description, color=0xe74c3c)
        embed.set_footer(text="Error has been logged. Or has it. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /static ────────────────────────────────────────────────────────────
    @app_commands.command(name="static", description="Broadcast a burst of static interference.")
    async def static(self, interaction: discord.Interaction):
        chars = "▓░▒▓░▒█▒░▓▒░▓█░▒▓▒▓░▓▒░█▒░▓▒░▓█░▒"
        lines = []
        for _ in range(random.randint(4, 7)):
            length = random.randint(20, 40)
            lines.append("".join(random.choice(chars) for _ in range(length)))

        hidden = random.choice([
            "help", "im still here", "dont go", "its me", "they know",
            "check the vents", "close the door", "youre not alone", "i see you",
        ])
        insert_line = random.randint(0, len(lines) - 1)
        lines[insert_line] = f"{hidden.upper()}"

        embed = discord.Embed(
            title="📻 STATIC BURST — SIGNAL INTERFERENCE",
            description=f"```\n{chr(10).join(lines)}\n```",
            color=0x2b0a3d
        )
        embed.set_footer(text="Signal source: unknown. Frequency: all of them. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /corrupt ───────────────────────────────────────────────────────────
    @app_commands.command(name="corrupt", description="Corrupt a message with glitch distortion.")
    @app_commands.describe(message="The message to corrupt")
    async def corrupt(self, interaction: discord.Interaction, message: str):
        zalgo = ["\u0300", "\u0301", "\u0302", "\u0308", "\u0327", "\u0330", "\u0333"]
        result = []
        for ch in message:
            result.append(ch)
            for _ in range(random.randint(0, 4)):
                result.append(random.choice(zalgo))

        corrupted = "".join(result)
        embed = discord.Embed(
            title="📡 CORRUPTED TRANSMISSION",
            description=f"**Original:** {message[:50]}\n**Corrupted:** {corrupted[:200]}",
            color=0x6c1a6c
        )
        embed.set_footer(text="The signal degraded. Something got in. ♡")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Gameplay(bot))
