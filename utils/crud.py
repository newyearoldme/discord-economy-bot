from sqlalchemy import select, func, update
from sqlalchemy.orm import Session
from typing import Optional, Literal

from .models import Users
from utils.db_alchemy import engine

from random import random, randint

# Economy.py

def get_user(discord_id: int) -> Optional[Users]:
    with Session(bind=engine) as session:
        return session.scalars(select(Users).where(Users.discord_id == discord_id)).first()


def get_balance(discord_id: int) -> Optional[int]:
    with Session(bind=engine) as session:
        return session.scalars(select(Users.balance).where(Users.discord_id == discord_id)).first()


def create_user(discord_id: int) -> Users:
    with Session(bind=engine) as session:
        user = Users(discord_id=discord_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def add_money(discord_id: int) -> tuple[Literal["not_registered", "success", "reset"]]:
    with Session(bind=engine) as session:
        user = session.scalars(select(Users).where(Users.discord_id == discord_id)).first()

        if not user:
            return "not_registered", None

        roll = random()
        if roll <= 0.9:
            amount = randint(100, 500)
            user.balance += amount
            session.commit()
            return "success", amount
        else:
            user.balance = 0
            session.commit()
            return "reset", None


def all_in(discord_id: int) -> tuple[Literal["zero_balance","not_registered", "success", "reset"]]:
    with Session(bind=engine) as session:
        user = session.scalars(select(Users).where(Users.discord_id == discord_id)).first()

        if user.balance == 0:
            return "zero_balance", None

        if not user:
            return "not_registered", None
        
        roll = random()
        if roll <= 0.5:
            user.balance *= 2
            session.commit()
            return "success", user.balance
        else:
            user.balance = 0
            session.commit()
            return "reset", 0


def transfer_money(sender_id: int, receiver_id: int, value: int) -> bool:
    with Session(bind=engine) as session:
        sender = session.scalars(select(Users).where(Users.discord_id == sender_id)).first()
        receiver = session.scalars(select(Users).where(Users.discord_id == receiver_id)).first()

        if not sender or not receiver:
            return False

        if sender.balance < value:
            return False

        sender.balance -= value
        receiver.balance += value

        session.commit()
        return True

# administrator.py

def admin_delete_user(discord_id: int) -> bool:
    with Session(bind=engine) as session:
        user = session.scalars(select(Users).where(Users.discord_id == discord_id)).first()

        if not user:
            return False

        session.delete(user)
        session.commit()
        return True


def admin_reset_money(discord_id: int) -> bool:
    with Session(bind=engine) as session:
        user = session.scalars(select(Users).where(Users.discord_id == discord_id)).first()

        if not user:
            return False

        user.balance = 0
        session.commit()
        return True

def admin_add_money(discord_id: int, amount: int):
    with Session(bind=engine) as session:
        user = session.scalars(select(Users).where(Users.discord_id == discord_id)).first()

        if not user:
            return False

        user.balance += amount
        session.commit()
        return True
    

def admin_add_all_money(amount: int) -> bool:
    with Session(bind=engine) as session:
        users = session.scalars(select(Users)).all()

        if not users:
            return False

        for user in users:
            user.balance += amount

        session.commit()
        return True


def reset_all_money():
    with Session(bind=engine) as session:
        session.query(Users).update({Users.balance: 0})
        session.commit()


def delete_all_users():
    with Session(bind=engine) as session:
        session.query(Users).delete()
        session.commit()


def get_all_balance() -> int:
    with Session(bind=engine) as session:
        return session.scalar(select(func.sum(Users.balance))) or 0


def get_all_users() -> int:
    with Session(bind=engine) as session:
        return session.scalar(select(func.count(Users.id))) or 0


def get_mid_balance() -> float:
    with Session(bind=engine) as session:
        total_balance = session.scalar(select(func.sum(Users.balance))) or 0
        total_users = session.scalar(select(func.count(Users.id))) or 0

        if total_users == 0:
            return 0.0

        return total_balance / total_users


def get_all_users_full():
    with Session(bind=engine) as session:
        result = session.execute(select(Users.id, Users.discord_id, Users.balance)).all()
        return result
