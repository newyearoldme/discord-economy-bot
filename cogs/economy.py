import discord
from discord import option
from discord.ext import commands

from utils import crud


class Economy(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Регистрирует Вас в базе данных")
    async def register(self, ctx: discord.ApplicationContext):
        user_in_db = await crud.get_user(ctx.author.id)
        if not user_in_db:
            await crud.create_user(ctx.author.id)
            await ctx.respond("✅ Вы успешно зарегистрировались!", ephemeral=True)
        else:
            await ctx.respond("❌ Вы уже зарегистрированы!", ephemeral=True)

    @discord.slash_command(description="Показывает Ваш баланс")
    async def balance(self, ctx: discord.ApplicationContext):
        balance = await crud.get_balance(ctx.author.id)

        if balance is None:
            await ctx.respond("❌ Вы не зарегистрированы, используйте команду `/register`", ephemeral=True)
        else:
            await ctx.respond(f"У Вас на балансе ${balance}", ephemeral=True)

    @discord.slash_command(description="90% шанс получить $100-500, 10% потерять всё")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def add_money(self, ctx: discord.ApplicationContext):
        result, value = await crud.add_money(ctx.author.id)

        match result:
            case "not_registered":
                await ctx.respond("❌ Вы не зарегистрированы, используйте команду `/register`", ephemeral=True)
            case "success":
                await ctx.respond(f"✅ Вам повезло, на ваш счёт добавлено ${value}", ephemeral=True)
            case "reset":
                await ctx.respond("💀 Неудача! Ваш счёт обнулён...", ephemeral=True)

    @discord.slash_command(description="Испытайте удачу, либо Ваш счёт удваивается, либо обнуляется!")
    async def all_in(self, ctx: discord.ApplicationContext):
        result, balance = await crud.all_in(ctx.author.id)

        match result:
            case "not_registered":
                await ctx.respond("❌ Вы не зарегистрированы, используйте команду `/register`", ephemeral=True)
            case "zero_balance":
                await ctx.respond("❌ Вы не можете делать all in при нулевом балансе", ephemeral=True)
            case "success":
                await ctx.respond(f"✅ Вам повезло, Ваш счёт удвоился, теперь он составляет ${balance}", ephemeral=True)
            case "reset":
                await ctx.respond("💀 Неудача! Ваш счёт обнулён...", ephemeral=True)

    @discord.slash_command(description="Перевести деньги другому пользователю")
    @option("value", description="Введите сумму для отправки", input_type=int, min_value=1)
    async def transfer_money(self, ctx: discord.ApplicationContext, user: discord.User, value: int):
        if user.bot:
            await ctx.respond("❌ Нельзя отправлять деньги боту!", ephemeral=True)
            return
        
        if user.id == ctx.author.id:
            await ctx.respond("❌ Нельзя отправлять деньги самому себе!", ephemeral=True)
            return

        success = await crud.transfer_money(ctx.author.id, user.id, value)

        if not success:
            await ctx.respond("⚠️ Невозможно выполнить перевод. Возможно, один из пользователей не зарегистрирован или недостаточно средств", ephemeral=True)
            return

        await ctx.respond(f"✅ Вы успешно перевели ${value} пользователю {user.mention}", ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(Economy(bot))
