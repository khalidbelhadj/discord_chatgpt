import discord
from discord.message import Message
from openai import OpenAI
import os

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if DISCORD_TOKEN is None: raise ValueError("Discord token not found.")

OPENAI_TOKEN = os.environ.get("OPENAI_TOKEN")
if OPENAI_TOKEN is None: raise ValueError("OpenAI token not found.")

openaiClient = OpenAI(api_key=OPENAI_TOKEN)

intents = discord.Intents.default()
intents.message_content = True
discordClient = discord.Client(intents=intents)

async def send_message(message: str, user_message: Message):
    try:
        await user_message.channel.send(message)
    except Exception as e:
        print(e)

def main():
    @discordClient.event
    async def on_message(user_message: Message):
        if user_message.author == discordClient.user: return
        query = str(user_message.content)
        print("Prompt:", query)

        await send_message("INFO: This bot does not remember previous messages", user_message)

        responses = [""]

        try:
            stream = openaiClient.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": query}],
                stream=True,
            )

            for chunk in stream:
                res = chunk.choices[0].delta.content
                if res is not None:
                    if len(responses[-1]) + len(res) > 2000:
                        responses.append("")
                    responses[-1] += res

        except Exception as e:
            print(e)

        if responses[0] == "":
            print("GPT4 unavailable")
            await send_message("GPT4 unavailable", user_message)

        for res in responses:
            await send_message(res, user_message)

        print("Responded successfully")

    discordClient.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
