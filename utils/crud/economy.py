from sqlalchemy import select, update, func
from enum import Enum

from ..models import Users
from ..db_alchemy import SessionLocal

from random import random, randint


class AddMoneyResult(str, Enum):
    NOT_REGISTERED = "not_registered"
    SUCCESS = "success"
    RESET = "reset"

class AllInResult(str, Enum):
    NOT_REGISTERED = "not_registered"
    SUCCESS = "success"
    RESET = "reset"
    ZERO_BALANCE = "zero_balance"

async def get_balance(discord_id: int) -> int | None:
    async with SessionLocal() as session:
        return await session.scalar(select(Users.balance).where(Users.discord_id == discord_id))

async def add_money(discord_id: int) -> tuple[AddMoneyResult, int | None]:
    async with SessionLocal() as session:
        user = await session.scalar(select(Users).where(Users.discord_id == discord_id))

        if not user:
            return AddMoneyResult.NOT_REGISTERED, None

        roll = random()
        if roll <= 0.9:
            amount = randint(100, 500)
            user.balance += amount
            await session.commit()
            return AddMoneyResult.SUCCESS, amount
        else:
            user.balance = 0
            await session.commit()
            return AddMoneyResult.RESET, None

async def all_in(discord_id: int) -> tuple[AllInResult, int | None]:
    async with SessionLocal() as session:
        user = await session.scalar(select(Users).where(Users.discord_id == discord_id))

        if not user:
            return AllInResult.NOT_REGISTERED, None

        if user.balance == 0:
            return AllInResult.ZERO_BALANCE, None
        
        roll = random()
        if roll <= 0.5:
            user.balance *= 2
        else:
            user.balance = 0
            
        await session.commit()
        return AllInResult.SUCCESS if roll <= 0.5 else AllInResult.RESET, user.balance

async def transfer_money(sender_id: int, receiver_id: int, value: int) -> bool:
    async with SessionLocal() as session:
        sender = await session.scalar(select(Users).where(Users.discord_id == sender_id))
        receiver = await session.scalar(select(Users).where(Users.discord_id == receiver_id))

        if not sender or not receiver:
            return False

        if sender.balance < value:
            return False

        sender.balance -= value
        receiver.balance += value

        await session.commit()
        return True

async def admin_reset_money(discord_id: int) -> bool:
    async with SessionLocal() as session:
        user = await session.scalar(select(Users).where(Users.discord_id == discord_id))

        if not user:
            return False

        user.balance = 0
        await session.commit()
        return True

async def admin_add_money(discord_id: int, amount: int):
    async with SessionLocal() as session:
        user = await session.scalar(select(Users).where(Users.discord_id == discord_id))

        if not user:
            return False

        user.balance += amount
        await session.commit()
        return True
    
async def admin_add_all_money(amount: int) -> bool:
    async with SessionLocal() as session:
        result = await session.scalars(select(Users))
        users = result.all()

        if not users:
            return False

        for user in users:
            user.balance += amount

        await session.commit()
        return True

async def reset_all_money():
    async with SessionLocal() as session:
        await session.execute(update(Users).values(balance=0))
        await session.commit()

async def get_all_balance() -> int:
    async with SessionLocal() as session:
        return await session.scalar(select(func.sum(Users.balance))) or 0

async def get_mid_balance() -> float:
    async with SessionLocal() as session:
        total_balance = await session.scalar(select(func.sum(Users.balance))) or 0
        total_users = await session.scalar(select(func.count(Users.id))) or 0

        if total_users == 0:
            return 0.0

        return total_balance / total_users
