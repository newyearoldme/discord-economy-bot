from utils import crud
import discord
from discord.ui import Modal, InputText


class AddMoneyModal(Modal):
    def __init__(self):
        super().__init__(title="Добавить деньги пользователю")
        self.add_item(InputText(label="ID пользователя", placeholder="1234567890"))
        self.add_item(InputText(label="Сумма", placeholder="100"))

    async def callback(self, interaction: discord.Interaction):
        user_id = int(self.children[0].value)
        amount = int(self.children[1].value)

        success = crud.admin_add_money(user_id, amount)
        if success:
            await interaction.response.send_message(f"✅ Добавлено ${amount} пользователю `{user_id}`", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Пользователь не найден", ephemeral=True)

class AddMoneyAllModal(Modal):
    def __init__(self):
        super().__init__(title="Добавить деньги всем пользователям")
        self.add_item(InputText(label="Сумма", placeholder="100"))

    async def callback(self, interaction: discord.Interaction):
        amount = int(self.children[0].value)

        success = crud.admin_add_all_money(amount)
        if success:
            await interaction.response.send_message(f"✅ Всем пользователям выдано ${amount}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ База данных пустая", ephemeral=True)

class ResetMoneyModal(Modal):
    def __init__(self):
        super().__init__(title="Обнулить счёт пользователю")
        self.add_item(InputText(label="ID пользователя", placeholder="1234567890"))

    async def callback(self, interaction: discord.Interaction):
        user_id = int(self.children[0].value)

        success = crud.admin_reset_money(user_id)
        if success:
            await interaction.response.send_message(f"✅ Счёт пользователя `{user_id}` обнулён!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Пользователь не найден", ephemeral=True)

class RemoveUserModal(Modal):
    def __init__(self):
        super().__init__(title="Удалить пользователя с базы")
        self.add_item(InputText(label="ID пользователя", placeholder="1234567890"))

    async def callback(self, interaction: discord.Interaction):
        user_id = int(self.children[0].value)

        success = crud.admin_delete_user(user_id)
        if success:
            await interaction.response.send_message(f"✅ Пользователь `{user_id}` удалён из базы данных!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Пользователь не найден", ephemeral=True)
