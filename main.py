import discord
import os
from keep_alive import keep_alive
import controller as ur
import meme
import encourage
import inspire
import random
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


client = discord.Client()

ur_controller = ur.UrController()

game_die = '\U0001f3b2'
new_piece = '\U0001f4e4'
end_turn_emoji = '\U0001f51a'

last = None
ur_game_last_message_id = -1


@client.event
async def on_ready():
    print('We have logged in as a {0.user}'.format(client))

    for guild in client.guilds:
        if guild.name == "Family Robot":
            for channel in guild.channels:
                if channel.name == "general":
                    await channel.send("I'm back")
                    # await run_play(channel)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global last
    global ur_game_last_message_id

    if last == 'meme' and message.content.lower() == 'yes':
        await meme.handle_yes(message)
        last = 'yes'
    elif last == 'meme' and message.content.lower() == 'no':
        await meme.handle_no(message)
        last = 'no'
    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        last = 'hello'
    elif message.content.startswith('$inspire'):
        await inspire.handle_inspire(message)
        last = 'quote'
    elif message.content.startswith('$meme'):
        await meme.handle_meme(message)
        last = 'meme'
    elif any(word in message.content for word in encourage.sad_words):
        await encourage.handle(message)
        last = "encourage"
    elif message.content.startswith("$gen meme"):
        await meme.generate_meme_loop(message)
        last = "gen meme"
    elif message.content.startswith("$stop gen"):
        await meme.end_meme_loop(message)
        last = "stop gen"
    elif message.content.startswith("$play ur"):
        ur_controller = ur.UrController()
        display, turn = await ur_controller.handle()
        embedVar = discord.Embed(
            title="The Game of Ur",
            color=0x00ff00,
            type="rich",
            author="Pasha")
        embedVar.add_field(name="Board", value=display, inline=True)
        embedVar.add_field(name="Turn", value=turn.name, inline=True)
        newMessage = await message.channel.send(embed=embedVar)
        await newMessage.add_reaction(game_die)
        ur_game_last_message_id = newMessage.id
    else:
        last = None


@client.event
async def on_reaction_add(reaction, user):
    global ur_game_last_message_id

    if user == client.user:
        return

    if ur_game_last_message_id != reaction.message.id:
        return

    if reaction.emoji == game_die:
        board, dice_roll, moves, turn = await ur_controller.roll_dice()
        message = reaction.message
        embedVar = discord.Embed(
            title="The Game of Ur",
            color=0x00ff00,
            type="rich",
            author="Pasha")
        embedVar.add_field(name="Board", value=board, inline=True)
        embedVar.add_field(name="Turn", value=turn.name, inline=True)
        embedVar.add_field(name="Dice Roll", value=dice_roll, inline=True)
        new_message = await message.channel.send(embed=embedVar)
        if moves == None:
            await new_message.add_reaction(new_piece)
        ur_game_last_message_id = new_message.id
    elif reaction.emoji == new_piece:
        new_message = await ur_controller.new_piece(reaction.message)
        ur_game_last_message_id = new_message.id
        await new_message.add_reaction(end_turn_emoji)
    elif reaction.emoji == end_turn_emoji:
        ur_controller.update_turn()
        board = ur_controller.get_printed_board()
        turn = ur_controller.get_turn()
        message = reaction.message
        embedVar = discord.Embed(
            title="The Game of Ur",
            color=0x00ff00,
            type="rich",
            author="Pasha")
        embedVar.add_field(name="Board", value=board, inline=True)
        embedVar.add_field(name="Turn", value=turn.name, inline=True)
        new_message = await message.channel.send(embed=embedVar)
        await new_message.add_reaction(game_die)
        ur_game_last_message_id = new_message.id


keep_alive()
client.run(os.getenv('TOKEN'))
