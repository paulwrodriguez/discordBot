import random

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there."
]

async def handle(message):
  await message.channel.send(random.choice(starter_encouragements))