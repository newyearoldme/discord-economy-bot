from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from .models import Users
from utils.db_alchemy import engine


def get_user(discord_id: int) -> Optional[Users]:
    with Session(bind=engine) as session:
        stmt = select(Users).where(Users.discord_id == discord_id)
        return session.scalars(stmt).first()


def get_balance(discord_id: int) -> Optional[int]:
    with Session(bind=engine) as session:
        stmt = select(Users.balance).where(Users.discord_id == discord_id)
        return session.scalars(stmt).first()


def create_user(discord_id: int) -> Users:
    with Session(bind=engine) as session:
        user = Users(discord_id=discord_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user(discord_id: int) -> bool:
    with Session(bind=engine) as session:
        stmt = select(Users).where(Users.discord_id == discord_id)
        user = session.scalars(stmt).first()

        if not user:
            return False

        session.delete(user)
        session.commit()
        return True


def add_money(discord_id: int, value: int) -> bool:
    with Session(bind=engine) as session:
        stmt = select(Users).where(Users.discord_id == discord_id)
        user = session.scalars(stmt).first()

        if not user:
            return False

        user.balance += value
        session.commit()
        return True


def reset_money(discord_id: int) -> bool:
    with Session(bind=engine) as session:
        stmt = select(Users).where(Users.discord_id == discord_id)
        user = session.scalars(stmt).first()

        if not user:
            return False

        user.balance = 0
        session.commit()
        return True


def transfer_money(sender_id: int, receiver_id: int, value: int) -> bool:
    with Session(bind=engine) as session:
        stmt_sender = select(Users).where(Users.discord_id == sender_id)
        stmt_receiver = select(Users).where(Users.discord_id == receiver_id)

        sender = session.scalars(stmt_sender).first()
        receiver = session.scalars(stmt_receiver).first()

        if not sender or not receiver:
            return False

        if sender.balance < value:
            return False

        sender.balance -= value
        receiver.balance += value

        session.commit()
        return True
