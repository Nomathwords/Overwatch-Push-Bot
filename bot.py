import discord
from br_item_shop import construct_shop_photo
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
    print(f'You have logged in as {client.user}')

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
        await message.channel.send(f"Hello {message.author.global_name}!")

    if message.content.startswith('hi'):
        await message.channel.send('Hi!')

    if message.content.startswith('hola'):
        await message.channel.send('¿Que tal?')

    if message.content.startswith("how's it hanging"):
        await message.channel.send('Just pushing this barrier')

    if message.content.startswith('sup') and not (message.content.startswith("super") or message.content.startswith("supper")):
        await message.channel.send("Yo yo yo what's up homeslice *does Fortnite's 'Fierce' emote*")

    if message.content.startswith('bonjour'):
        await message.channel.send("Comment vas-tu?")

    if message.content.startswith('yo') and not message.content.startswith("you"):
        await message.channel.send("Yo, you chillin'?")

    if "hewwo" in message.content:
        await message.channel.send("haiiiii omg ^_^ hi!! hiiiiii <3 haiiiiii hii :3")

    if message.content.startswith('uwu'):
        await message.channel.send("ᵘʷᵘ oh frick ᵘʷᵘ ᵘʷᵘ \n ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ \n ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ frick sorry guys \n ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ \n \
                                   ᵘʷᵘ ᵘʷᵘ sorry im dropping \n ᵘʷᵘ my uwus all over the \n ᵘʷᵘ place ᵘʷᵘ ᵘʷᵘ ᵘʷᵘ sorry")

    if message.content.startswith('howdy'):
        await message.channel.send("Howdy howdy howdy")

    if message.content.startswith("hello bro"):
        await message.channel.send("I'm a freak, just lmk...")

# Test command to make Push Bot say hello
@tree.command(
    name = "testcommand",
    description = "I'm testing a slash command! This will make Push Bot say hello!",
)
async def testcommand(interaction):
    await interaction.response.send_message("Hello!")

# Command to make Push Bot add numbers
@tree.command(
        description = "He can't do your taxes, but he can add!"
)
@app_commands.describe(
    first_value = "The first value you want to add something to",
    second_value = "The value you want to add to the first value",
    third_value = "The value you want to add to the second value"
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int, third_value: Optional[int]):
    third_value = third_value or 0
    await interaction.response.send_message(f'{first_value} + {second_value} + {third_value} = {first_value + second_value + third_value}')

# Command to create a poll in chat
@tree.command(
    description = "Poll your friends!"
)
@app_commands.describe(
    question = "The question of the poll",
    one = "The first value in the poll",
    two = "The second value in the poll",
    three = "The third value in the poll",
    four = "The fourth value in the poll"
)
async def poll(interaction: discord.Interaction, question: str, one: str, two: str, three: Optional[str], four: Optional[str]):

    # Get optional parmeters, if any
    three = three or None
    four = four or None

    # Build the poll in a dictionary and remove the interaction value
    my_poll = locals()
    del my_poll['interaction']

    # Variables
    returned_message = ""
    emojis = ['🇦', '🇧', '🇨', '🇩']

    # Remove any keys with values of None
    for key, value in list(my_poll.items()):
        if value == None:
            del my_poll[key]

    # Create the poll message by looping through our values and appending them to the message variable
    for i in range (0, len(my_poll)):
        if list(my_poll.keys())[i] == "question":
            returned_message = returned_message + list(my_poll.values())[i] + "\n"

        # We use [i - 1] on the emojis array to access the first emoji, even though we are on the second my_poll element
        else:
            returned_message = returned_message + emojis[i - 1] + " - " + list(my_poll.values())[i] + "\n"

    returned_message.strip()

    # Send the poll message
    poll_message = await interaction.response.send_message(returned_message)

    # Get the message that was just sent originally
    my_sent_message = await interaction.original_response()

    # Add reactions to the poll message
    for emoji in emojis[:len(my_poll) - 1]:  # React only to the number of options provided
        await my_sent_message.add_reaction(emoji)

# Command to make Push Bot retrieve the Item Shop
@tree.command(
    name = "shop",
    description = "Retrieve the current Fortnite BR item shop"
)
async def fetch_br_shop(interaction: discord.Interaction):

    # This request will take more than 3 seconds, so we need to defer it first to not get an error
    await interaction.response.defer()

    # Get the shop
    return_statement = construct_shop_photo()

    # Send the shop in chat
    await interaction.followup.send(return_statement)
        
# This needs the bot's token, which only Hunter has
client.run('')