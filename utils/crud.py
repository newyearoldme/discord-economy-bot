from typing import Optional
from utils.models import Users


async def get_user_by_discord_id(discord_id: int) -> Optional[Users]:
    return await Users.get_or_none(discord_id = discord_id)

async def create_user(discord_id: int) -> Users:
    return await Users.create(discord_id = discord_id)

async def delete_user(discord_id: int) -> bool:
    user = await get_user_by_discord_id(discord_id)
    if user:
        await user.delete()
        return True
    return False
