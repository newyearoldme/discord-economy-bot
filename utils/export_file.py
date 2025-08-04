import discord
from io import StringIO
from utils import crud


async def export_users_file(client: discord.Client) -> discord.File:
    users = crud.get_all_users_full()
    file = StringIO()
    file.write("ID | Имя пользователя         | Баланс\n")
    file.write("-" * 50 + "\n")
    for user_id, discord_id, balance in users:
        user = client.get_user(discord_id)
        name = user.name if user else "Неизвестен"
        file.write(f"{str(user_id).ljust(2)} | {name.ljust(24)} | ${balance}\n")

    file.seek(0)
    return discord.File(file, filename="users.txt")
