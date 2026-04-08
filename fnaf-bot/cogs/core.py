import discord
from discord.ext import commands
from discord import app_commands
import random
import platform


class Core(commands.Cog):
    """Core commands — help, ping, userinfo."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /help ──────────────────────────────────────────────────────────────
    @app_commands.command(name="help", description="Display the training tape — all available commands.")
    async def help_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📼 TRAINING TAPE — NIGHT GUARD ORIENTATION",
            description=(
                "*Static crackles… a grainy recording begins.*\n\n"
                "Hello, hello? Uh, welcome to your new position.\n"
                "Here is a list of… tools at your disposal. Good luck."
            ),
            color=0x2b0a3d
        )
        embed.add_field(
            name="🎥 Core",
            value=(
                "`/help` — You're watching it\n"
                "`/ping` — System latency check\n"
                "`/userinfo` — Scan a user's file"
            ),
            inline=False
        )
        embed.add_field(
            name="🔒 Security System",
            value=(
                "`/cameras` — View a security feed\n"
                "`/power` — Check power levels\n"
                "`/status` — Animatronic status report\n"
                "`/night` — Begin your night shift\n"
                "`/jumpscare` — Something is watching\n"
                "`/quote` — A transmission from the dark"
            ),
            inline=False
        )
        embed.add_field(
            name="🧸 Characters",
            value=(
                "`/character [name]` — Pull a character file\n"
                "`/characters` — List all known entities\n"
                "`/summon [name]` — Call an animatronic\n"
                "`/voice [name]` — Hear a character quote\n"
                "`/whoisnear` — Detect nearby animatronics"
            ),
            inline=False
        )
        embed.add_field(
            name="🔒 Immersion",
            value=(
                "`/lockdoor` — Seal a security door\n"
                "`/unlockdoor` — Reopen the door\n"
                "`/lights` — Check hallway lights\n"
                "`/vent` — Inspect the ventilation\n"
                "`/hide` — Attempt to hide"
            ),
            inline=False
        )
        embed.add_field(
            name="🎲 Random Events",
            value=(
                "`/event` — Trigger a random event\n"
                "`/danger` — Current threat level\n"
                "`/timer` — Current in-game time"
            ),
            inline=False
        )
        embed.add_field(
            name="🎮 Gameplay",
            value=(
                "`/startshift [night]` — Begin your night shift\n"
                "`/endshift` — End the shift\n"
                "`/checkpower` — Power consumption report\n"
                "`/survivalrate` — Odds of making it\n"
                "`/log [note]` — File a night log entry\n"
                "`/report` — Generate an incident report\n"
                "`/scan [user]` — Run a security scan"
            ),
            inline=False
        )
        embed.add_field(
            name="📡 Glitch / Horror",
            value=(
                "`/glitch [text]` — Glitch a transmission\n"
                "`/error` — System failure message\n"
                "`/static` — Broadcast static interference\n"
                "`/corrupt [text]` — Distort a message"
            ),
            inline=False
        )
        embed.add_field(
            name="⚠️ Extras",
            value=(
                "`/haunt [user]` — Send a haunting\n"
                "`/survive` — Will you make it?\n"
                "`/checkcams` — Full camera sweep\n"
                "`/jumpscare` — Something is watching\n"
                "`/quote` — A transmission from the dark"
            ),
            inline=False
        )
        embed.add_field(
            name="🎀 Cute-Creepy",
            value=(
                "`/watchme` — I'm watching you ♡\n"
                "`/staywithme` — Please don't go ♡\n"
                "`/promise` — A binding promise ♡"
            ),
            inline=False
        )
        embed.add_field(
            name="⚙️ Setup (prefix commands)",
            value=(
                "`!setchannel #channel` — Send all ambient messages to a specific channel\n"
                "`!setchannel` — Use the current channel\n"
                "`!clearchannel` — Reset to default (first available channel)\n"
                "*Requires `Manage Channels` permission.*"
            ),
            inline=False
        )
        embed.set_footer(text="They're not supposed to hurt you… they just forget. ♡")
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/freddy-fazbears-pizza/images/d/dd/Freddy_Fazbear_ref_sheet_by_joltgametravel.png")
        await interaction.response.send_message(embed=embed)

    # ── /ping ──────────────────────────────────────────────────────────────
    @app_commands.command(name="ping", description="System latency check.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        if latency < 100:
            status = "All systems nominal. ✅"
            color = 0x9b59b6
        elif latency < 200:
            status = "Minor interference detected… ⚠️"
            color = 0xe67e22
        else:
            status = "C̷o̷n̷n̷e̷c̷t̷i̷o̷n̷ u̷n̷s̷t̷a̷b̷l̷e̷… ❌"
            color = 0xe74c3c

        embed = discord.Embed(
            title="📡 SYSTEM PING",
            description=f"**Latency:** `{latency}ms`\n**Status:** {status}",
            color=color
        )
        embed.set_footer(text="The cameras are always watching.")
        await interaction.response.send_message(embed=embed)

    # ── /userinfo ──────────────────────────────────────────────────────────
    @app_commands.command(name="userinfo", description="Scan a user like a security system log.")
    @app_commands.describe(user="The user to scan (leave blank to scan yourself)")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()
        try:
            target = user or interaction.user

            if interaction.guild and not isinstance(target, discord.Member):
                target = interaction.guild.get_member(target.id) or target

            age_days = (discord.utils.utcnow() - target.created_at).days
            if age_days < 30:
                threat = "🔴 HIGH — New account detected"
            elif age_days < 365:
                threat = "🟡 MODERATE — Observed"
            else:
                threat = "🟢 LOW — Familiar face"

            is_member = isinstance(target, discord.Member)
            joined_str = f"<t:{int(target.joined_at.timestamp())}:R>" if is_member and target.joined_at else "Unknown"

            if is_member:
                all_roles = [r.mention for r in reversed(target.roles) if r.name != "@everyone"]
                roles_str = ""
                for r in all_roles:
                    candidate = roles_str + (", " if roles_str else "") + r
                    if len(candidate) > 950:
                        remaining = len(all_roles) - all_roles.index(r)
                        roles_str += f" *+{remaining} more*"
                        break
                    roles_str = candidate
                if not roles_str:
                    roles_str = "No roles assigned"
            else:
                roles_str = "No roles assigned"

            embed = discord.Embed(
                title="📋 SECURITY SCAN — USER FILE",
                description=f"*Scanning… movement detected.*\n\nTarget acquired: **{target.display_name}**",
                color=0x2b0a3d
            )
            embed.set_thumbnail(url=target.display_avatar.url)
            embed.add_field(name="🪪 ID", value=f"`{target.id}`", inline=True)
            embed.add_field(name="🤖 Bot?", value="Yes" if target.bot else "No", inline=True)
            embed.add_field(name="📅 Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=False)
            embed.add_field(name="📥 Joined Server", value=joined_str, inline=False)
            embed.add_field(name="🎭 Roles", value=roles_str, inline=False)
            embed.add_field(name="⚠️ Threat Level", value=threat, inline=False)
            embed.set_footer(text="I always remember a face. ♡")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="⚠️ SCAN FAILURE",
                    description=f"*Static… unable to retrieve file.*\n\n`{e}`",
                    color=0xe74c3c
                )
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
