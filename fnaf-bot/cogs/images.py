import discord
from discord.ext import commands
from discord import app_commands
import random

# ── Image URL arrays ─────────────────────────────────────────────────────────
# Add more URLs to any array to expand the pool

# Steam CDN — official FNAF game artwork, always publicly accessible
_STEAM = "https://cdn.akamai.steamstatic.com/steam/apps"

PFP_IMAGES = [
    f"{_STEAM}/319510/header.jpg",          # FNAF 1
    f"{_STEAM}/332800/header.jpg",          # FNAF 2
    f"{_STEAM}/354140/header.jpg",          # FNAF 3
    f"{_STEAM}/388090/header.jpg",          # FNAF 4
    f"{_STEAM}/506610/header.jpg",          # Sister Location
    f"{_STEAM}/738060/header.jpg",          # Pizzeria Simulator
    f"{_STEAM}/871720/header.jpg",          # Ultimate Custom Night
    f"{_STEAM}/747660/header.jpg",          # Security Breach
    f"{_STEAM}/2287450/header.jpg",         # Security Breach Ruin
    f"{_STEAM}/1070110/header.jpg",         # Help Wanted
]

BANNER_IMAGES = [
    f"{_STEAM}/319510/capsule_616x353.jpg",
    f"{_STEAM}/332800/capsule_616x353.jpg",
    f"{_STEAM}/354140/capsule_616x353.jpg",
    f"{_STEAM}/388090/capsule_616x353.jpg",
    f"{_STEAM}/506610/capsule_616x353.jpg",
    f"{_STEAM}/747660/capsule_616x353.jpg",
    f"{_STEAM}/1070110/capsule_616x353.jpg",
    f"{_STEAM}/2287450/capsule_616x353.jpg",
]

FANART_IMAGES = [
    f"{_STEAM}/319510/capsule_616x353.jpg",   # FNAF 1
    f"{_STEAM}/332800/capsule_616x353.jpg",   # FNAF 2
    f"{_STEAM}/354140/capsule_616x353.jpg",   # FNAF 3
    f"{_STEAM}/388090/capsule_616x353.jpg",   # FNAF 4
    f"{_STEAM}/506610/capsule_616x353.jpg",   # Sister Location
    f"{_STEAM}/738060/capsule_616x353.jpg",   # Pizzeria Simulator
    f"{_STEAM}/871720/capsule_616x353.jpg",   # Ultimate Custom Night
    f"{_STEAM}/747660/capsule_616x353.jpg",   # Security Breach
    f"{_STEAM}/1070110/capsule_616x353.jpg",  # Help Wanted
    f"{_STEAM}/2287450/capsule_616x353.jpg",  # Security Breach Ruin
]


class Images(commands.Cog):
    """Image commands — pfp, banner, fanart."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /pfp ──────────────────────────────────────────────────────────────
    @app_commands.command(name="pfp", description="Send a FNAF-style profile picture.")
    async def pfp(self, interaction: discord.Interaction):
        url = random.choice(PFP_IMAGES)
        embed = discord.Embed(
            title="🖼️ FNAF Profile Picture",
            description="*Retrieved from the archive. Use it wisely.*",
            color=0x2b0a3d
        )
        embed.set_image(url=url)
        embed.set_footer(text="They're always watching. Might as well look the part. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /banner ────────────────────────────────────────────────────────────
    @app_commands.command(name="banner", description="Send a FNAF-style banner image.")
    async def banner(self, interaction: discord.Interaction):
        url = random.choice(BANNER_IMAGES)
        embed = discord.Embed(
            title="🎑 FNAF Banner",
            description="*Pulled from the security archive.*",
            color=0x2b0a3d
        )
        embed.set_image(url=url)
        embed.set_footer(text="Freddy Fazbear's Pizza — Where Fantasy and Fun Come to Life!")
        await interaction.response.send_message(embed=embed)

    # ── /fanart ────────────────────────────────────────────────────────────
    @app_commands.command(name="fanart", description="Send a random FNAF image.")
    async def fanart(self, interaction: discord.Interaction):
        url = random.choice(FANART_IMAGES)
        embed = discord.Embed(
            title="🎨 FNAF Image",
            description="*Something was found in the archives.*",
            color=0x2b0a3d
        )
        embed.set_image(url=url)
        embed.set_footer(text="Art retrieved from classified storage. ♡")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Images(bot))
