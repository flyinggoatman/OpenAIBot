from decouple import config
import discord
import openai

TOKEN = config('TOKEN', str)
AI_TOKEN = config('AI_TOKEN', str)
DISCORD_CHANNEL = config('DISCORD_CHANNEL', int)


intents = discord.Intents.all()
client = discord.Client(intents=intents)

openai_api_key = AI_TOKEN

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    openai.api_key = openai_api_key
    DISCORD_CHANNEL_int = int(DISCORD_CHANNEL)
    prompt = (f'{message.content}')
    if message.content.startswith("!ask") or isinstance(message.channel, discord.DMChannel):
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )
    message_to_send = completions.choices[0].text
    if isinstance(message.channel, discord.DMChannel):
        await message.author.send(message_to_send)
    else:
        if DISCORD_CHANNEL_int == message.channel.id:
            await message.channel.send(message_to_send)

client.run(TOKEN)
