from typing import Final
import os
import re 
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
import openai
from responses import get_response, is_greeting_message

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY: Final[str] = os.getenv('OPENAI_API_KEY')  # Load OpenAI API key

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Helper function to check if a query is about Rowan University.
def is_rowan_related(query: str) -> bool:
    keywords = ['rowan', 'glassboro', 'university']
    return any(keyword in query.lower() for keyword in keywords)

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    # Check if the message is private (indicated by a prefix '?')
    is_private = False
    if user_message[0] == '?':
        is_private = True
        user_message = user_message[1:]
    
    # Get the response using stateful conversation logic.
    response: str = get_response(user_message, str(message.author.id))
    try:
        if is_private:
            await message.author.send(response)
        else:
            # For channel responses, prepend the user's mention.
            await message.channel.send(f"{message.author.mention} {response}")
    except Exception as e:
        print(e)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    # Ignore messages from the bot itself.
    if message.author == client.user:
        return

    # Check if the message is a DM (message.guild is None)
    if message.guild is None:
        print("DM:", message.content)
        await send_message(message, message.content)
        return

    # Restrict bot responses to the "bot-testing" channel in a guild.
    if not hasattr(message.channel, 'name') or message.channel.name != "bot-testing":
        return

    # Use the original message content to check for greetings anywhere.
    content = message.content.strip()
    is_greeting = is_greeting_message(content)
    is_mentioned = client.user in message.mentions

    # Only respond if there's a greeting anywhere in the message or if the bot is mentioned.
    if not is_greeting and not is_mentioned:
        return

    print(message.content)
    await send_message(message, message.content)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
