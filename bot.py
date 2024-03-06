import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Sync the tree commands
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    await tree.sync()
    print("Ready!")

# Send messages based on chat keywords
@client.event
async def on_message(message):

    message.content = message.content.lower()

    # Ignore all messages from Push Bot
    if message.author == client.user:
        return

    if message.content.startswith('hello') and not message.content.startswith('hello '):
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

    if message.content.startswith('yo') and not message.content.startswith("you"):
        await message.channel.send("Yo, you chillin'?")

    if message.content.startswith('hewwo'):
        await message.channel.send("haiiiii omg ^_^ hi!! hiiiiii <3 haiiiiii hii :3")

    if message.content.startswith('uwu'):
        await message.channel.send("ᵘʷᵘ oh frick ᵘʷᵘ ᵘʷᵘ \n ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ \n ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ frick sorry guys \n ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ \n ᵘʷᵘ ᵘʷᵘ sorry im dropping \n ᵘʷᵘ my uwus all over the \n ᵘʷᵘ place ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ sorry")

    if message.content.startswith('howdy'):
        await message.channel.send("Howdy howdy howdy")

    if message.content.startswith("hello bro"):
        await message.channel.send("I'm a freak, just lmk...")

# Test command to make Push Bot say hello
@tree.command(
    name = "testcommand",
    description = "I'm testing a slash command! This will make the bot say hello!",
)
async def testcommand(interaction):
    await interaction.response.send_message("Hello!")

# Command to make Push Bot add numbers
@tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
    third_value = 'The value you want to add to the second value'
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int, third_value: Optional[int]):
    """Adds two numbers together."""
    third_value = third_value or 0
    await interaction.response.send_message(f'{first_value} + {second_value} + {third_value} = {first_value + second_value + third_value}')

# Command to create a poll in chat
@tree.command()
@app_commands.describe(
    question = 'The question of the poll',
    one = "The first value in the poll",
    two = "The second value in the poll",
    three = "The third value in the poll",
    four = "The fourth value in the poll"
)
async def poll(interaction: discord.Interaction, question: str, one: str, two: str, three: Optional[str], four: Optional[str]):
    
    # Get optional parmeters, if any
    three = three or None
    four = four or None

    # Build array of question and poll values
    my_poll = []
        

client.run('')