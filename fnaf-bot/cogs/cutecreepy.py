import discord
from discord.ext import commands
from discord import app_commands
import random

# ── Character summon responses ─────────────────────────────────────────────────
SUMMON_RESPONSES = {
    "freddy fazbear": [
        "The stage lights flicker. Freddy's head turns slowly toward you.\n*\"Hello there, little friend. We've been expecting you. ♡\"*",
        "A low, familiar laugh echoes from the hallway.\n*\"Ha. Ha. Ha. There you are. I always find my guests eventually.\"*",
        "Freddy steps into the light, top hat tilted, eyes fixed on you.\n*\"The show must go on. And tonight… you're the star.\"*",
    ],
    "bonnie": [
        "Something moves in the shadows near the left door. A pair of glowing eyes.\n*\"Hey there. Hope you don't mind. I let myself in. ♡\"*",
        "You hear guitar strings. Slowly. Deliberately.\n*\"I've been watching you all night. Just wanted to say hi.\"*",
        "Bonnie stands in the doorway, guitar slung over his shoulder.\n*\"You look tired. You should get some rest. I'll keep watch.\"*",
    ],
    "chica": [
        "The kitchen sounds stop. Then footsteps. Then silence.\n*\"Let's eat! ♡ You haven't eaten, have you? You look pale.\"*",
        "Chica appears with her cupcake, head slightly tilted.\n*\"Mr. Cupcake wanted to meet you. He's been asking about you all night.\"*",
        "A warm smell of something baking drifts through the office.\n*\"I made something for you. Don't worry about what's in it. ♡\"*",
    ],
    "foxy": [
        "The curtain at Pirate Cove splits open. Foxy emerges, running.\n*\"Ahoy, matey! Ye should've been watching Cove. Lesson learned. ♡\"*",
        "Something sprints down the hall. It stops just outside.\n*\"Found ye. Foxy always finds what he's looking for.\"*",
        "A raspy voice from the hallway:\n*\"I've been waiting, mate. Waiting a long time. Good things come to those who wait.\"*",
    ],
    "golden freddy": [
        "The lights cut out. When they return, a golden suit sits slumped in the corner.\n*\"…\"*\n*It stares. That's all. That's enough.*",
        "The air feels wrong. Heavy. The poster on the wall has changed.\n*\"…it's me.\"*",
        "You blink. Golden Freddy is in the office. You blink again.\n*He's gone. But the feeling isn't.*",
    ],
    "springtrap": [
        "The ventilation groans. The cameras glitch.\n*\"I always come back. You know that by now. ♡\"*",
        "A shape moves in the corner of CAM 3. It looks back.\n*\"Did you think this was over? It's never over.\"*",
        "Springtrap steps into view, withered suit shifting.\n*\"I've been here since the beginning. I'll be here at the end.\"*",
    ],
    "circus baby": [
        "A recorded voice begins to play, sweet and clear:\n*\"I remember you. I remember everything. I think about you often. ♡\"*",
        "Baby's massive frame fills the doorway.\n*\"Do you want to hear a secret? It's a good one. It's about you.\"*",
        "The lights dim to red. Baby smiles.\n*\"I've been saving a spot for you. Right here. Don't be afraid.\"*",
    ],
    "ballora": [
        "Music begins. Slow, graceful, wrong.\n*\"Why do you always come here? You know what happens. ♡\"*",
        "Ballora pirouettes into the room, eyes closed.\n*\"Close your eyes too. It's easier that way. I promise.\"*",
        "The melody grows louder. She's close.\n*\"Stay still. Stay quiet. Let me find you.\"*",
    ],
    "nightmare fredbear": [
        "The bedroom grows cold. Something very large is smiling in the darkness.\n*\"I will put you back together. ♡\"*",
        "The bed creaks. Nightmare Fredbear leans in close.\n*\"Shh. It's just a dream. Dreams can't hurt you. Usually.\"*",
        "Every light in the room dies.\n*\"You can't run from nightmares, child. You know that. Deep down. ♡\"*",
    ],
    "vanny": [
        "Someone waves from across the parking lot. White bunny suit. No context.\n*\"Hi. ♡ I've been watching you for a while now. Just wanted you to know.\"*",
        "You hear breathing through the speaker system.\n*\"Don't look for me. You won't find me. But I'll find you.\"*",
        "A figure ducks behind a shelf just as you turn.\n*\"Peek-a-boo. ♡ I see you.\"*",
    ],
    "sun moon": [
        "☀️ Sun leans in close, bells jingling:\n*\"OH HI!! Welcome to daycare! Art time? Music time? Fun time? ♡\"*\n\n🌑 Then the lights go out.\n*\"…Lights out. Time for sleep. Whether you want to or not.\"*",
        "The Daycare Attendant waves cheerfully from the ceiling.\n☀️ *\"Up here! Hi hi hi!\"*\n🌑 *\"…The lights are going to go out soon. Just so you know. ♡\"*",
    ],
    "glitchtrap": [
        "Something in the game data moved on its own.\n*\"I don't want to scare you. I just want to stay. Forever. ♡\"*",
        "The VR environment glitches. A golden rabbit stands in the void.\n*\"You collected all the tapes. Thank you. That's all I needed.\"*",
        "He waves. Friendly. Normal. Wrong.\n*\"Hi there. I've been inside this game for a long time. You're the first one to really listen. ♡\"*",
    ],
}

DEFAULT_SUMMON = [
    "The lights flicker. Something stirs.\n*\"Did you call for me? I heard. I always hear. ♡\"*",
    "A presence fills the room. Cold, patient, watching.\n*\"You shouldn't have done that. They don't like being called.\"*",
    "The building groans. Whatever you summoned is on its way.\n*\"I hope you know what you did. ♡\"*",
]

# ── Character voice lines ──────────────────────────────────────────────────────
CHARACTER_VOICES = {
    "freddy fazbear": [
        "\"Welcome to Freddy Fazbear's Pizza, where fantasy and fun come to life!\"",
        "\"Ha. Ha. Ha.\"",
        "\"The show must go on. For all of us.\"",
        "\"I always know where my guests are. Every single one of them. ♡\"",
    ],
    "bonnie": [
        "\"Hey there, sport. You're doing great. Mostly.\"",
        "\"I don't sleep. Neither should you. Just a thought.\"",
        "\"The left hallway is mine. I thought you should know.\"",
    ],
    "chica": [
        "\"Let's eat! ♡\"",
        "\"The kitchen is very important. Don't ask what we make.\"",
        "\"Mr. Cupcake says hi. He's always watching. Isn't that sweet?\"",
    ],
    "foxy": [
        "\"Ahoy there, matey! Foxy's the name, and speed's me game!\"",
        "\"Ye should've been watching Pirate Cove more carefully. Lesson learned.\"",
        "\"I run. That's all I do. Fast and certain and inevitable. ♡\"",
    ],
    "golden freddy": [
        "\"…it's me.\"",
        "\"…\"",
        "\"You know what you did.\"",
        "\"We were there. In the beginning. ♡\"",
    ],
    "springtrap": [
        "\"I always come back.\"",
        "\"You can't kill something that's already dead. Almost.\"",
        "\"I've been in worse situations. I'll be fine. You won't be. ♡\"",
    ],
    "circus baby": [
        "\"I remember everything. Every smile. Every face. Every soul. ♡\"",
        "\"Do you want to hear a story? It's a good one. It ends with you.\"",
        "\"I was made to perform. I take that very seriously.\"",
    ],
    "ballora": [
        "\"Why do you come here? You know what happens to people who come here. ♡\"",
        "\"Close your eyes. It's easier that way. I've been told.\"",
        "\"My music is for you. It always has been.\"",
    ],
    "nightmare fredbear": [
        "\"I. Will. Put. You. Back. Together. ♡\"",
        "\"This is all just a dream. Isn't that comforting?\"",
        "\"Hush now. The nightmare isn't real. Mostly.\"",
    ],
    "vanny": [
        "\"Do you see me? I see you. ♡\"",
        "\"I'm not supposed to talk about what I do. But I can smile about it.\"",
        "\"He chose me, you know. Out of everyone. I'm very grateful. ♡\"",
    ],
    "glitchtrap": [
        "\"I don't want to be forgotten. That's all I ask. ♡\"",
        "\"The game is real. That's the trick. It was always real.\"",
        "\"You collected all the tapes. Good. That's exactly what I needed.\"",
    ],
    "sun moon": [
        "☀️ \"HI HI HI!! Art time! Fun time! BEST time!! ♡\"",
        "🌑 \"…The lights are going to go out. Sleep now.\"",
        "☀️ \"No no no! No leaving the daycare!\" 🌑 \"…There's nowhere to go anyway.\"",
    ],
}

DEFAULT_VOICE = [
    "\"I've been watching you for a very long time. ♡\"",
    "\"They never really leave, you know. This place. They stay.\"",
    "\"You shouldn't be here after hours. But I'm glad you are.\"",
    "\"The building has a memory. So do we. ♡\"",
]

# ── Nearby animatronic pool ─────────────────────────────────────────────────────
NEARBY = [
    ("Freddy Fazbear", "👀 He's in the hallway. Laughing softly to himself."),
    ("Bonnie", "🐰 Left door. Pressed against the wall. Waiting."),
    ("Chica", "🐥 She's in the kitchen. You can hear her moving."),
    ("Foxy", "🦊 Pirate Cove curtain is open. He's already gone."),
    ("Golden Freddy", "💛 The office feels heavy. He's here. Somewhere."),
    ("Mangle", "🔧 Static on all cameras. She's in the ceiling."),
    ("The Puppet", "🎭 The music box is slowing. She's almost free."),
    ("Springtrap", "🐰 CAM 3 shows movement. He's looking right at the camera."),
    ("Ballora", "🩰 Her music is getting louder. She knows you're here."),
    ("Nightmare Fredbear", "🌑 The lights won't turn on. He doesn't need them."),
    ("Vanny", "🐇 Something white moved across the parking lot camera. Then nothing."),
    ("Nightmare", "⬛ There's nothing in the room. That's how you know."),
]

# ── Cute-creepy responses ──────────────────────────────────────────────────────
WATCHME = [
    "👁️ *I've been watching you for a while now. You have a nice face. ♡*",
    "📷 *CAM 4B has been trained on your location since you arrived. Don't look up.*",
    "🌑 *You felt it, didn't you? That feeling of being watched. That's real. That's me. ♡*",
    "👀 *I watched you walk in. I watched you sit down. I'm watching right now. ♡*",
    "🎥 *The cameras never turn off. I made sure of that. Just for you.*",
]

STAYWITHME = [
    "🧸 *Don't go. Please? There's so much night left. Just a little longer. ♡*",
    "🌙 *The building gets lonely after hours. You make it less so. Stay. I'll keep you safe.*",
    "🐻 *I won't let anything happen to you. I promise. You belong here. ♡*",
    "🎵 *If you leave, the music stops. And when the music stops… well. You know. Don't leave. ♡*",
    "💜 *Just one more hour. That's all. You can survive one more hour with me. Can't you?*",
]

PROMISE = [
    "🤝 *I promise I'll never let anything hurt you. Not while I'm here. And I'm always here. ♡*",
    "🔒 *You are safe. I made sure the doors won't open for anyone else. Just us. ♡*",
    "🐇 *I promise to find you. No matter where you go. That's not a threat. That's a comfort. ♡*",
    "🌸 *I will protect you forever. You didn't ask for that. But here we are. ♡*",
    "💛 *Cross my heart. Which is still here, somewhere. I kept it for you. ♡*",
]


class CuteCreepy(commands.Cog):
    """Character interaction and cute-creepy commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /summon ────────────────────────────────────────────────────────────
    @app_commands.command(name="summon", description="Call upon an animatronic. They will respond.")
    @app_commands.describe(character="The character to summon (e.g. freddy, bonnie, springtrap)")
    async def summon(self, interaction: discord.Interaction, character: str = None):
        if character:
            key = character.strip().lower()
            responses = SUMMON_RESPONSES.get(key, DEFAULT_SUMMON)
        else:
            all_entries = list(SUMMON_RESPONSES.values())
            responses = random.choice(all_entries)

        char_display = character.title() if character else "Unknown Entity"
        embed = discord.Embed(
            title=f"🕯️ SUMMONING — {char_display}",
            description=random.choice(responses),
            color=0x2b0a3d
        )
        embed.set_footer(text=f"Summoned by {interaction.user.display_name}. You asked for this. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /voice ─────────────────────────────────────────────────────────────
    @app_commands.command(name="voice", description="Hear a quote from a specific character.")
    @app_commands.describe(character="The character to quote (e.g. freddy, ballora, glitchtrap)")
    async def voice(self, interaction: discord.Interaction, character: str = None):
        if character:
            key = character.strip().lower()
            quotes = CHARACTER_VOICES.get(key, DEFAULT_VOICE)
            char_display = character.title()
        else:
            key = random.choice(list(CHARACTER_VOICES.keys()))
            quotes = CHARACTER_VOICES[key]
            char_display = key.title()

        embed = discord.Embed(
            title=f"🎙️ {char_display.upper()} SPEAKS",
            description=random.choice(quotes),
            color=0x6c1a6c
        )
        embed.set_footer(text="Recording captured. Source confirmed. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /whoisnear ─────────────────────────────────────────────────────────
    @app_commands.command(name="whoisnear", description="Detect which animatronic is closest to you.")
    async def whoisnear(self, interaction: discord.Interaction):
        count = random.randint(1, 3)
        nearby = random.sample(NEARBY, count)

        embed = discord.Embed(
            title="🔎 PROXIMITY DETECTION — ACTIVE",
            description="*Scanning nearby sectors…*",
            color=0x2b0a3d
        )
        for name, location in nearby:
            embed.add_field(name=f"🤖 {name}", value=location, inline=False)

        if count >= 3:
            embed.add_field(name="⚠️ WARNING", value="Multiple entities detected in your vicinity. Close the doors.", inline=False)
        embed.set_footer(text="They were always near. You just didn't know. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /watchme ───────────────────────────────────────────────────────────
    @app_commands.command(name="watchme", description="They're watching. They want you to know.")
    async def watchme(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=f"{random.choice(WATCHME)}\n\n— *{interaction.user.mention}*",
            color=0x2b0a3d
        )
        embed.set_footer(text="You can feel it, can't you? ♡")
        await interaction.response.send_message(embed=embed)

    # ── /staywithme ────────────────────────────────────────────────────────
    @app_commands.command(name="staywithme", description="Please don't go. It's cold here alone. ♡")
    async def staywithme(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=random.choice(STAYWITHME),
            color=0x6c1a6c
        )
        embed.set_footer(text="Sent with love. And something else. ♡")
        await interaction.response.send_message(embed=embed)

    # ── /promise ───────────────────────────────────────────────────────────
    @app_commands.command(name="promise", description="A promise. Binding. Permanent. ♡")
    async def promise(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=random.choice(PROMISE),
            color=0x2b0a3d
        )
        embed.set_footer(text="Promises made here are kept. Always. ♡")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CuteCreepy(bot))
