import discord
from discord.ext import commands
import asyncio
import os

from tortoise import Tortoise

from dotenv import load_dotenv
load_dotenv()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents, loop=loop)

token = os.getenv("token")

if not token:
    raise RuntimeError("❌ Не найден токен в переменных окружения")

cogs_list = [
    'economy'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    print("Бот работает!")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.respond(
            "❌ У Вас нет прав администратора для использования этой команды",
            ephemeral=True
        )
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"❌ Команда на перезарядке, попробуйте через {round(error.retry_after, 2)} сек.", ephemeral=True)
    else:
        print(f"❗ Ошибка: {error}")
        await ctx.respond("⚠️ Произошла неизвестная ошибка.", ephemeral=True)

async def main():
    await Tortoise.init(db_url="sqlite://utils/db.sqlite", modules={"discord": ["utils.models"]})
    await Tortoise.generate_schemas()
    await bot.login(token)
    await bot.connect()

try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(Tortoise.close_connections())
