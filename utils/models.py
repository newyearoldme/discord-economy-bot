from tortoise.models import Model
from tortoise.fields import IntField, BigIntField


class Users(Model):
    id = IntField(primary_key=True)
    discord_id = BigIntField(unique=True)
    balance = IntField(default=0)
