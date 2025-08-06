from utils import crud
import discord
from discord.ui import Modal, InputText
from typing import Optional, Callable, Any, Tuple

class BaseAdminModal(Modal):
    def __init__(self, title: str, inputs: list[Tuple[str, str]]):
        super().__init__(title=title)
        for label, placeholder in inputs:
            self.add_item(InputText(label=label, placeholder=placeholder))
    
    async def handle_action(
        self, 
        interaction: discord.Interaction, 
        action_func: Callable[[Any], bool],
        success_message: str,
        error_message: str = "❌ Пользователь не найден",
        *args
    ) -> None:
        try:
            success = action_func(*args)
            if success:
                await interaction.response.send_message(success_message, ephemeral=True)
            else:
                await interaction.response.send_message(error_message, ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Неверный формат данных", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Произошла ошибка: {str(e)}", ephemeral=True)

class AddMoneyModal(BaseAdminModal):
    def __init__(self):
        super().__init__(
            title="Добавить деньги пользователю",
            inputs=[
                ("ID пользователя", "1234567890"),
                ("Сумма", "100")
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        user_id = int(self.children[0].value)
        amount = int(self.children[1].value)
        
        await self.handle_action(
            interaction=interaction,
            action_func=crud.admin_add_money,
            success_message=f"✅ Добавлено ${amount} пользователю `{user_id}`",
            user_id=user_id,
            amount=amount
        )

class AddMoneyAllModal(BaseAdminModal):
    def __init__(self):
        super().__init__(
            title="Добавить деньги всем пользователям",
            inputs=[("Сумма", "100")]
        )

    async def callback(self, interaction: discord.Interaction):
        amount = int(self.children[0].value)
        
        await self.handle_action(
            interaction=interaction,
            action_func=crud.admin_add_all_money,
            success_message=f"✅ Всем пользователям выдано ${amount}",
            error_message="❌ База данных пустая",
            amount=amount
        )

class ResetMoneyModal(BaseAdminModal):
    def __init__(self):
        super().__init__(
            title="Обнулить счёт пользователю",
            inputs=[("ID пользователя", "1234567890")]
        )

    async def callback(self, interaction: discord.Interaction):
        user_id = int(self.children[0].value)
        
        await self.handle_action(
            interaction=interaction,
            action_func=crud.admin_reset_money,
            success_message=f"✅ Счёт пользователя `{user_id}` обнулён!",
            user_id=user_id
        )

class RemoveUserModal(BaseAdminModal):
    def __init__(self):
        super().__init__(
            title="Удалить пользователя с базы",
            inputs=[("ID пользователя", "1234567890")]
        )

    async def callback(self, interaction: discord.Interaction):
        user_id = int(self.children[0].value)
        
        await self.handle_action(
            interaction=interaction,
            action_func=crud.admin_delete_user,
            success_message=f"✅ Пользователь `{user_id}` удалён из базы данных!",
            user_id=user_id
        )
