import os
import re

import discord
from dotenv import load_dotenv

from erb_logic import generate_response


intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


def _is_reply_to_bot(message: discord.Message) -> bool:
    if not message.reference or not message.reference.message_id:
        return False

    referenced = message.reference.resolved
    if referenced is None:
        return False

    if not isinstance(referenced, discord.Message):
        return False

    return bool(referenced.author and bot.user and referenced.author.id == bot.user.id)


def _is_mentioning_bot(message: discord.Message) -> bool:
    return bool(bot.user and bot.user in message.mentions)


def _extract_prompt(message: discord.Message) -> str:
    if not bot.user:
        return message.content

    cleaned = re.sub(rf"<@!?{bot.user.id}>", "", message.content)
    return cleaned.strip()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if not (_is_mentioning_bot(message) or _is_reply_to_bot(message)):
        return

    prompt = _extract_prompt(message)
    if not prompt:
        prompt = "hi"

    response = generate_response(prompt)
    await message.channel.send(response)


def main() -> None:
    load_dotenv()
    # Ensure only one instance runs
    lockfile = os.path.join(tempfile.gettempdir(), 'discord_bot.lock')
    try:
        lockfd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        os.write(lockfd, str(os.getpid()).encode())
    except FileExistsError:
        print("Another instance is already running.")
        sys.exit(1)

    try:
        token = os.getenv("DISCORD_BOT_TOKEN")
        token = token.replace(">", "3")
        if not token:
            raise RuntimeError("DISCORD_BOT_TOKEN is not set (check your .env file)")
        bot.run(token)
    finally:
        try:
            os.close(lockfd)
            os.remove(lockfile)
        except Exception:
            pass


if __name__ == "__main__":
    main()
