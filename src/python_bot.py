import discord
from discord.ext import commands
import threading

from boka import booking_agent, wait_till_midnight_callback
from env import discord_token


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    if bot.user == message.author:
        return

    await bot.process_commands(message)


@bot.command(name="book", help="books at the given intervals")
async def most_recent(payload):
    if payload.author == bot.user:
        return

    args = message = payload.message.content.split(" ")[1:]

    await payload.channel.send(
        "Då Bokar jag vid intervall " + " och ".join(", ".join(args).rsplit(", ", 1)),
    )

    def callback():
        booking_agent(args, payload.channel.send)

    thread = threading.Thread(target=wait_till_midnight_callback, args=(callback,))
    thread.start()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f"{ctx.message.content} finns inte", delete_after=15)
        await ctx.message.delete(delay=10)


@bot.event
async def on_command_error2(ctx, error):
    await ctx.send("kommand error", delete_after=15)
    await ctx.message.delete(delay=10)


bot.run(discord_token)
