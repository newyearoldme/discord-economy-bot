import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.db_alchemy import init_db

load_dotenv()

init_db()

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

token = os.getenv("token")

if not token:
    raise RuntimeError("❌ Не найден токен в переменных окружения")

cogs_list = [
    'administrator',
    'economy'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    print("✅ Бот работает!")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.respond(
            "❌ У Вас нет прав администратора для использования этой команды",
            ephemeral=True
        )
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            f"❌ Команда на перезарядке, попробуйте через {round(error.retry_after, 2)} сек.", ephemeral=True)
    else:
        print(f"❗ Ошибка: {error}")
        await ctx.respond("⚠️ Произошла неизвестная ошибка.", ephemeral=True)

if __name__ == "__main__":
    bot.run(token)
