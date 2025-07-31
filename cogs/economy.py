import discord
from discord import option
from discord.ext import commands

from typing import Optional
from utils import crud


class Economy(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Регистрирует Вас в базе данных")
    async def register(self, ctx: discord.ApplicationContext):
        user_in_db = crud.get_user(ctx.author.id)
        if not user_in_db:
            crud.create_user(ctx.author.id)
            await ctx.respond("✅ Вы успешно зарегистрировались!", ephemeral=True)
        else:
            await ctx.respond("❌ Вы уже зарегистрированы!", ephemeral=True)

    @discord.slash_command(description="Показывает баланс")
    async def get_balance(self, ctx: discord.ApplicationContext, user: Optional[discord.User] = None):
        user = user or ctx.author
        balance = crud.get_balance(user.id)

        if balance is None:
            if user.id == ctx.author.id:
                await ctx.respond("❌ Вы не зарегистрированы, используйте команду `/register`", ephemeral=True)
            else:
                await ctx.respond(f"❌ Пользователь {user.mention} не зарегистрирован", ephemeral=True)
            return

        if user.id == ctx.author.id:
            await ctx.respond(f"У Вас на балансе ${balance}", ephemeral=True)
        else:
            await ctx.respond(f"Баланс {user.mention}: ${balance}", ephemeral=True)

    @discord.slash_command(description="Добавляет деньги на Ваш счёт (таймаут - 10 сек.)")
    @option("value", input_type=int, description="Введите сумму пополнения", min_value=1)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def add_money(self, ctx: discord.ApplicationContext, value: int, user: Optional[discord.User] = None):
        user = user or ctx.author
        success = crud.add_money(user.id, value)

        if not success:
            if user.id == ctx.author.id:
                await ctx.respond("❌ Вы не зарегистрированы, используйте команду `/register`", ephemeral=True)
            else:
                await ctx.respond(f"❌ Пользователь {user.mention} не зарегистрирован", ephemeral=True)
            return

        if user.id == ctx.author.id:
            await ctx.respond(f"✅ На Ваш счёт добавлено ${value}", ephemeral=True)
        else:
            await ctx.respond(f"✅ На счёт {user.mention} добавлено ${value}", ephemeral=True)

    @discord.slash_command(description="Перевести деньги другому пользователю")
    @option("value", description="Введите сумму для отправки", input_type=int, min_value=1)
    async def transfer_money(self, ctx: discord.ApplicationContext, user: discord.User, value: int):
        if user.id == ctx.author.id:
            await ctx.respond("❌ Нельзя отправлять деньги самому себе!", ephemeral=True)
            return

        success = crud.transfer_money(ctx.author.id, user.id, value)

        if not success:
            await ctx.respond("⚠️ Невозможно выполнить перевод. Возможно, один из пользователей не зарегистрирован или недостаточно средств.", ephemeral=True)
            return

        await ctx.respond(f"✅ Вы успешно перевели ${value} пользователю {user.mention}", ephemeral=True)

    @discord.slash_command(description="Обнуляет счёт пользователя")
    async def reset_balance(self, ctx: discord.ApplicationContext, user: Optional[discord.User] = None):
        user = user or ctx.author
        success = crud.reset_money(user.id)

        if not success:
            if user.id == ctx.author.id:
                await ctx.respond("⚠️ Вы не зарегестрированы", ephemeral=True)
            else:
                await ctx.respond(f"⚠️ Пользователь {user.mention} не зарегистрирован", ephemeral=True)
                return  
            
        if user.id == ctx.author.id:
            await ctx.respond("✅ Ваш счёт обнулён!", ephemeral=True)
        else:
            await ctx.respond(f"✅ Счёт пользователя {user.mention} обнулён!", ephemeral=True)

    @discord.slash_command(description="Удаляет пользователя из базы данных")
    async def remove_user(self, ctx: discord.ApplicationContext, user: Optional[discord.User] = None):
        user = user or ctx.author     
        deleted = crud.delete_user(user.id)

        if not deleted:
            if user.id == ctx.author.id:
                await ctx.respond("⚠️ Вы не зарегестрированы", ephemeral=True)
            else:
                await ctx.respond(f"⚠️ Пользователь {user.mention} не зарегистрирован", ephemeral=True)
            return

        if user.id == ctx.author.id:
            await ctx.respond("✅ Вы успешно удалили себя из базы", ephemeral=True)
        else:
            await ctx.respond(f"✅ Пользователь {user.mention} удалён из базы", ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Economy(bot))
