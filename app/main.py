import random
from os import environ

import discord
from discord.ext import commands
from server import server_thread

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="!")
tree = bot.tree


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}.")
    await tree.sync()
    print("Synced slash commands.")


@tree.command(
    name="rps",
    description="グー、チョキ、パーを指定またはランダムに出力します",
)
async def rps(ctx: discord.Interaction, choice: int = None):
    choices = ["グー", "チョキ", "パー"]
    if choice is None:
        result = random.choice(choices)
    elif choice in [0, 1, 2]:
        result = choices[choice]
    else:
        await ctx.response.send_message(
            "無効な選択です。0, 1, 2のいずれかを指定してください。"
        )
        return

    embed = discord.Embed(title=f"{ctx.user.name}: {result}")
    await ctx.response.send_message(embed=embed)


@tree.command(
    name="dice",
    description="指定された数の6面ダイスを振ります",
)
async def dice(ctx: discord.Interaction, count: int):
    if count < 1:
        await ctx.response.send_message("自然数を指定してください。")
        return
    results = [random.randint(1, 6) for _ in range(count)]
    result_text = ", ".join(map(str, results))
    embed = discord.Embed(title=f"{ctx.user.name}のダイス結果", description=result_text)
    await ctx.response.send_message(embed=embed)


server_thread()
bot.run(environ["TOKEN"])
