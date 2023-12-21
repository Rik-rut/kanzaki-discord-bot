import nextcord
from nextcord.ext import commands
import json
import random
from settings import *

intents = nextcord.Intents.all()
bot = commands.Bot (command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print ("Bot is now online!")

@bot.event
async def on_message(message):
    channel = bot.get_channel(channel_id)
    if message.author == bot.user:
        return
    elif message.author.bot:
        return
    
    if message.channel.id != channel_id:
        return

    file_path = "data.json"
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    question = message.content.lower()
    matching_answers = [data["answer"] for data in existing_data if data.get("question") == question]
    if matching_answers:
        for answer in matching_answers:
            async with channel.typing():
                await channel.send (random.choice(answer))
    else:
        async with channel.typing():
            await channel.send(f"Try using '/learn' my slash commands to teach me a new response")

@bot.slash_command(description="Learn")
async def learn(ctx, question: str, answer: str):
    file_path = "data.json"
    
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_item = next((item for item in existing_data if item["question"] == question), None)
    for item in existing_data:
        if isinstance(item["answer"], str):
            item["answer"] = [item["answer"]]  # Convert single answer string to a list

    # Store the new data
    if existing_item:
        # Question already exists, append the answer
        existing_item["answer"].append(answer)  # Assuming answer is a list
    else:
        # New question, create a new entry with a list of answers
        new_data = {
            "question": question,
            "answer": [answer]  # Start with a list containing the new answer
        }
        existing_data.append(new_data)

    # Save the updated data to the file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    await ctx.send("Thanks for teaching me sensei!")
    print(f"Data has been added and saved to {file_path}")


# learn.default_member_permissions = nextcord.Permissions(administrator=True)

bot.run (bot_token)