# This example requires the 'message_content' intent.

import discord

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    message.content = message.content.lower()

    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('hi'):
        await message.channel.send('Hi!')

    if message.content.startswith('hola'):
        await message.channel.send('¿Que tal?')

    if message.content.startswith("how's it hanging"):
        await message.channel.send('Just pushing this barrier')

    if message.content.startswith('sup'):
        await message.channel.send("Yo yo yo what's up homeslice *does Fortnite's 'Fierce' emote*")

    if message.content.startswith('bonjour'):
        await message.channel.send("Comment vas-tu?")

    if message.content.startswith('yo'):
        await message.channel.send("Drop a beat homie")

client.run('')