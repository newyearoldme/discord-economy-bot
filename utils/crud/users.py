from sqlalchemy import select, delete, func

from ..models import Users
from ..db_alchemy import SessionLocal


async def get_user(discord_id: int) -> Users | None:
    async with SessionLocal() as session:
        return await session.scalar(select(Users).where(Users.discord_id == discord_id))
    
async def create_user(discord_id: int) -> Users:
    async with SessionLocal() as session:
        user = Users(discord_id=discord_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
async def delete_all_users():
    async with SessionLocal() as session:
        await session.execute(delete(Users))
        await session.commit()

async def get_all_users() -> int:
    async with SessionLocal() as session:
        return await session.scalar(select(func.count(Users.id))) or 0

async def get_all_users_full():
    async with SessionLocal() as session:
        result = await session.execute(select(Users.id, Users.discord_id, Users.balance))
        return result.all()
    
async def admin_delete_user(discord_id: int) -> bool:
    async with SessionLocal() as session:
        user = await session.scalar(select(Users).where(Users.discord_id == discord_id))

        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True
