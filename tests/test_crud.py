import pytest
from utils.models import Base
from utils.db_alchemy import engine
from utils import crud

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_user():
    user = crud.create_user(123)
    assert user.discord_id == 123

    fetched_user = crud.get_user(123)
    assert fetched_user is not None
    assert fetched_user.discord_id == 123

def test_add_money():
    crud.create_user(321)
    success = crud.add_money(321, 500)
    assert success is True

    balance = crud.get_balance(321)
    assert balance == 500

def test_transfer_money():
    crud.create_user(1)
    crud.create_user(2)
    crud.add_money(1, 100)

    result = crud.transfer_money(1, 2, 50)
    assert result is True

    assert crud.get_balance(1) == 50
    assert crud.get_balance(2) == 50

def test_transfer_fail_if_not_enough_money():
    crud.create_user(3)
    crud.create_user(4)
    crud.add_money(3, 10)

    result = crud.transfer_money(3, 4, 100)
    assert result is False

def test_remove_user():
    user = crud.create_user(5)
    assert user.discord_id == 5

    success = crud.delete_user(5)
    assert success == True

def test_reset_balance():
    crud.create_user(10)

    success = crud.reset_money(10)
    assert success == True
