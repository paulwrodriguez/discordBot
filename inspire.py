import requests
import json
import discord


async def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


async def handle_inspire(message):
    quote = await get_quote()
    await message.channel.send(quote)
