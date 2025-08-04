import discord
from utils import crud
from utils.export_file import export_users_file
from discord.ui import View, button
from .modals import AddMoneyAllModal, RemoveUserModal, AddMoneyModal, ResetMoneyModal


class AdminPanelView(View):
    @button(label="Обнулить всех", style=discord.ButtonStyle.danger, row=0)
    async def resetAllCallback(self, button, interaction: discord.Interaction):
        crud.reset_all_money()
        await interaction.response.send_message("✅ Все счета обнулены", ephemeral=True)

    @button(label="Обнулить счёт пользователю", style=discord.ButtonStyle.blurple, row=0)
    async def resetCallback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(ResetMoneyModal())

    @button(label="Удалить всех", style=discord.ButtonStyle.danger, row=1)
    async def deleteAllCallback(self, button, interaction: discord.Interaction):
        crud.delete_all_users()
        await interaction.response.send_message("✅ Все пользователи удалены с базы данных", ephemeral=True)

    @button(label="Удалить пользователя", style=discord.ButtonStyle.blurple, row=1)
    async def removeCallback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(RemoveUserModal())

    @button(label="Добавить всем денег", style=discord.ButtonStyle.green, emoji="💸", row=2)
    async def addAllCallback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(AddMoneyAllModal())

    @button(label="Добавить денег пользователю", style=discord.ButtonStyle.blurple, emoji="💸", row=2)
    async def addCallback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(AddMoneyModal())

    @button(label="Экспортировать пользователей", style=discord.ButtonStyle.secondary, row=3)
    async def export_users_callback(self, button, interaction: discord.Interaction):
        users = crud.get_all_users_full()
        if not users:
            await interaction.response.send_message("Пользователи не найдены", ephemeral=True)
            return
        
        file = await export_users_file(interaction.client)
        await interaction.response.send_message("📄 Пользователи:", file=file, ephemeral=True)

def get_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Админ панель",
    )
    embed.add_field(name=f"Общий баланс: ${crud.get_all_balance()}", value="", inline=False)
    embed.add_field(name=f"Количество учасников: {crud.get_all_users()}", value="")
    embed.add_field(name=f"Средний баланс: ${crud.get_mid_balance()}", value="")

    return embed

