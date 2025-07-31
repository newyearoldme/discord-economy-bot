from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import BigInteger

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    balance: Mapped[int] = mapped_column(default=0)
