import discord
import asyncio
import random
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

# Replace this with the user ID you want to mute/unmute
GUILD_ID = SET_GUILD_ID_HERE
TARGET_USER_ID = SET_DISCORD_TARGET_ID_HERE
BOT_TOKEN = 'SET_DISCORD_TOKEN_HERE'

@client.event
async def on_ready():
    print(f'[*] Logged in as {Fore.GREEN}{client.user.name}{Style.RESET_ALL}')
    client.loop.create_task(mute_user())

async def mute_user():
    await client.wait_until_ready()
    while not client.is_closed():
        guild = client.get_guild(GUILD_ID)
        if guild:
            member = guild.get_member(TARGET_USER_ID)
            if member:
                voice_state = member.voice
                if voice_state and voice_state.channel:
                    # Check if we should disconnect the user with a 1/100 chance
                    if random.randint(1, 100) == 1:
                        await member.move_to(None)
                        print(f'{Style.RESET_ALL}[*] {Fore.GREEN}{member.name}{Style.RESET_ALL} has been disconnected from the voice channel.')
                    else:
                        # Mute the user for a random duration
                        await member.edit(mute=True)
                        mute_duration = random.randint(10, 30)
                        print(f'{Style.RESET_ALL}[*] Muted {Fore.GREEN}{member.name}{Style.RESET_ALL} for {Fore.BLUE}{mute_duration}{Style.RESET_ALL} seconds.')
                        await asyncio.sleep(mute_duration)

                        # Unmute the user for a random duration
                        await member.edit(mute=False)
                        unmute_duration = random.randint(30, 90)
                        print(f'{Style.RESET_ALL}[*] Unmuted {Fore.GREEN}{member.name}{Style.RESET_ALL} for {Fore.BLUE}{unmute_duration}{Style.RESET_ALL} seconds.')
                        await asyncio.sleep(unmute_duration)
        await asyncio.sleep(1)

@client.event
async def on_voice_state_update(member, before, after):
    if member.id == TARGET_USER_ID:
        if after.channel and not before.channel:
            client.loop.create_task(mute_user())

client.run(BOT_TOKEN)
