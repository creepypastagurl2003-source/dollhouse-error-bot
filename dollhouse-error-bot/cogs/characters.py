import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random


# Load character data from JSON file
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "characters.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    CHARACTERS: dict = json.load(f)


class Characters(commands.Cog):
    """Character system — pull files on any FNAF animatronic."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /character ─────────────────────────────────────────────────────────
    @app_commands.command(name="character", description="Pull a character file. Leave blank for a random animatronic.")
    @app_commands.describe(name="Character name (e.g. Freddy, Springtrap, Vanny)")
    async def character(self, interaction: discord.Interaction, name: str = None):
        if name is None:
            # Random character
            key = random.choice(list(CHARACTERS.keys()))
        else:
            key = name.lower().strip()
            # Fuzzy match — check if the key is contained anywhere
            if key not in CHARACTERS:
                matches = [k for k in CHARACTERS if key in k or k in key]
                if matches:
                    key = matches[0]
                else:
                    await interaction.response.send_message(
                        f"❌ No file found for **{name}**. Try `/characters` to see all available entries.",
                        ephemeral=True
                    )
                    return

        char = CHARACTERS[key]
        embed = discord.Embed(
            title=f"📁 FILE: {char['name']}",
            description=f"*Accessing restricted archive…*",
            color=0x2b0a3d
        )
        embed.add_field(name="🎮 Game", value=char["game"], inline=True)
        embed.add_field(name="📄 Description", value=char["description"], inline=False)
        embed.add_field(name="⚙️ Behavior", value=char["behavior"], inline=False)
        embed.set_image(url=char["image"])
        embed.set_footer(text="This information is classified. You didn't find this. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /characters ────────────────────────────────────────────────────────
    @app_commands.command(name="characters", description="List all known animatronics in the archive.")
    async def characters(self, interaction: discord.Interaction):
        # Group by game
        games: dict[str, list[str]] = {}
        for data in CHARACTERS.values():
            game = data["game"]
            games.setdefault(game, []).append(data["name"])

        embed = discord.Embed(
            title="🗂️ ENTITY ARCHIVE — ALL KNOWN FILES",
            description="*The following entities have been catalogued. Approach with caution.*",
            color=0x2b0a3d
        )
        for game, names in games.items():
            embed.add_field(
                name=f"📼 {game}",
                value="\n".join(f"• {n}" for n in names),
                inline=True
            )
        embed.set_footer(text=f"{len(CHARACTERS)} entities on file. Some files may be missing. ♡")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Characters(bot))
