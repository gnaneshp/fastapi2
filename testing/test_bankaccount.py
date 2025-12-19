import pytest
from bankaccount import BankAccount

@pytest.fixture
def zero_balance_account():
    return BankAccount()

@pytest.fixture
def balance_account():
    return BankAccount(50)

def test_default_balance(zero_balance_account):
    assert zero_balance_account.balance==0
def test_account_balance(balance_account):
    assert balance_account.balance==50
def test_withdraw(balance_account):
    balance_account.withdraw(20)
    assert balance_account.balance==30
def test_deposit(balance_account):
    balance_account.deposit(30)
    assert balance_account.balance==80
def test_collect_interest(balance_account):
    balance_account.collect_interest()
    assert round(balance_account.balance,2)==55
def test_exception(balance_account):
    with pytest.raises(Exception):
        balance_account.withdraw(100)