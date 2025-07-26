import discord
from discord import option
from discord.ext import commands

from typing import Optional

from utils import crud
from tortoise.transactions import in_transaction


class Economy(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Регистрирует Вас в базе данных")
    async def register_user(self, ctx: discord.ApplicationContext):
        user_in_db = await crud.get_user_by_discord_id(ctx.author.id)
        if not user_in_db:
            await crud.create_user(ctx.author.id)
            await ctx.respond("✅ Вы успешно зарегистрировались!", ephemeral=True)
        else:
            await ctx.respond("❌ Вы уже зарегистрированы!", ephemeral=True)

    @discord.slash_command(description="Показывает баланс")
    async def get_balance(self, ctx: discord.ApplicationContext, user: Optional[discord.User] = None):
        user = user or ctx.author
        user_in_db = await crud.get_user_by_discord_id(user.id)

        if not user_in_db:
            if user.id == ctx.author.id:
                await ctx.respond("❌ Вы не зарегистрированы, используйте команду `register_user`", ephemeral=True)
            else:
                await ctx.respond(f"❌ Пользователь {user.mention} не зарегистрирован", ephemeral=True)
            return

        if user.id == ctx.author.id:
            await ctx.respond(f"У Вас на балансе ${user_in_db.balance}", ephemeral=True)
        else:
            await ctx.respond(f"Баланс {user.mention}: ${user_in_db.balance}", ephemeral=True)

    @discord.slash_command(description="Добавляет деньги на Ваш счёт")
    @option("value", input_type=int, description="Введите сумму пополнения", min_value=1)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def add_money(self, ctx: discord.ApplicationContext, value: int, user: Optional[discord.User] = None):
        user = user or ctx.author
        user_in_db = await crud.get_user_by_discord_id(user.id)

        if user_in_db is None:
            if user.id == ctx.author.id:
                await ctx.respond("❌ Вы не зарегистрированы, используйте `register_user`", ephemeral=True)
            else:
                await ctx.respond(f"❌ Пользователь {user.mention} не зарегистрирован", ephemeral=True)
            return

        user_in_db.balance += value
        await user_in_db.save()

        if user.id != ctx.author.id and not ctx.author.guild_permissions.administrator:
            await ctx.respond("❌ Вы не можете добавлять деньги другим пользователям", ephemeral=True)
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

        sender = await crud.get_user_by_discord_id(ctx.author.id)
        receiver = await crud.get_user_by_discord_id(user.id)

        if not sender or not receiver:
            await ctx.respond("⚠️ Один из пользователей не зарегистрирован!", ephemeral=True)
            return

        if sender.balance < value:
            await ctx.respond("❌ У вас недостаточно средств!", ephemeral=True)
            return

        async with in_transaction():
            sender.balance -= value
            receiver.balance += value
            await sender.save()
            await receiver.save()

        await ctx.respond(f"✅ Вы успешно перевели {value} пользователю {user.mention}", ephemeral=True)

    @discord.slash_command(description="Обнуляет счёт пользователя")
    @commands.has_permissions(administrator=True)
    async def reset_balance(self, ctx: discord.ApplicationContext, user: Optional[discord.User] = None):
        user = user or ctx.author
        user_in_db = await crud.get_user_by_discord_id(user.id)

        if not user_in_db:
            await ctx.respond("⚠️ Пользователь не зарегистрирован!", ephemeral=True)
            return

        user_in_db.balance = 0
        await user_in_db.save()

        if user.id == ctx.author.id:
            await ctx.respond("✅ Ваш счёт обнулён!", ephemeral=True)
        else:
            await ctx.respond(f"✅ Счёт пользователя {user.mention} обнулён!", ephemeral=True)

    @discord.slash_command(description="Удаляет пользователя из базы данных")
    @commands.has_permissions(administrator=True)
    async def remove_user(self, ctx: discord.ApplicationContext, user: Optional[discord.User] = None):
        user = user or ctx.author
        deleted = await crud.delete_user(user.id)

        if not deleted:
            if user.id == ctx.author.id:
                await ctx.respond(f"⚠️ Вы не зарегестрированы", ephemeral=True)
            else:
                await ctx.respond(f"⚠️ Пользователь {user.mention} не найден в базе", ephemeral=True)
            return

        if user.id == ctx.author.id:
            await ctx.respond(f"✅ Вы успешно удалили себя из базы", ephemeral=True)
        else:
            await ctx.respond(f"✅ Пользователь {user.mention} удалён из базы", ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Economy(bot))
