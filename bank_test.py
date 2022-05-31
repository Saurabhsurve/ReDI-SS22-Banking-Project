import pytest
# import user_defined_exceptions
from user_defined_exceptions import InvalidUserName, InvalidPassword, InvalidBalance, UserExists, UserNotFound,\
    InsufficientBalance

from helper_functions import username_valid, password_valid
from bank_classes import Customer, Account
from datetime import datetime


def test_username_valid():
    username = "Abc123"
    expected_status = True

    # Check whether username entered is valid
    assert(username_valid(username) == expected_status)


def test_username_invalid_length():
    username = "Max12"
    expected_status = False

    # Check whether username entered is valid
    assert(username_valid(username) == expected_status)


def test_username_invalid_blank():
    username = "      "
    expected_status = False

    # Check whether username entered is valid
    assert(username_valid(username) == expected_status)


def test_username_invalid_no_number():
    username = "Maximilian"
    expected_status = False

    # Check whether username entered is valid
    assert(username_valid(username) == expected_status)


def test_username_invalid_no_alphabet():
    username = "123456"
    expected_status = False

    # Check whether username entered is valid
    assert(username_valid(username) == expected_status)


def test_password_valid():
    username = "Abc@123"
    expected_status = True

    # Check whether password entered is valid
    assert(password_valid(username) == expected_status)


def test_password_invalid_length():
    username = "Max@1"
    expected_status = False

    # Check whether password entered is valid
    assert(password_valid(username) == expected_status)


def test_password_invalid_blank():
    username = "      "
    expected_status = False

    # Check whether password entered is valid
    assert(password_valid(username) == expected_status)


def test_password_invalid_no_number():
    username = "Max@milian"
    expected_status = False

    # Check whether password entered is valid
    assert(password_valid(username) == expected_status)


def test_password_invalid_no_alphabet():
    username = "123@56"
    expected_status = False

    # Check whether password entered is valid
    assert(password_valid(username) == expected_status)


def test_password_invalid_no_special_character():
    username = "Max123"
    expected_status = False

    # Check whether password entered is valid
    assert(password_valid(username) == expected_status)


def test_customer_signup_valid():
    # create unique username based on date time
    now = datetime.now()
    date_string = now.strftime("%y%m%d%H%M")
    username = "s" + date_string
    password = "Sunny@123"
    name = "Sunny G"
    address = "Melbourne"
    phone_number = 12345
    balance = 500

    cust_obj_signup = Customer.customer_signup(username, password, name, address, phone_number, balance)

    assert isinstance(cust_obj_signup, Customer)


def test_customer_signup_exception_invalid_username():
    username = "Max"
    password = "Max@123"
    name = "Max Kissel"
    address = "Munich"
    phone_number = 12345
    balance = 500

    with pytest.raises(InvalidUserName):
        Customer.customer_signup(username, password, name, address, phone_number, balance)


def test_customer_signup_exception_invalid_password():
    username = "Max123"
    password = "Max123"
    name = "Max Kissel"
    address = "Munich"
    phone_number = 12345
    balance = 500

    with pytest.raises(InvalidPassword):
        Customer.customer_signup(username, password, name, address, phone_number, balance)


def test_customer_signup_exception_invalid_balance_char():
    username = "Max123"
    password = "Max@123"
    name = "Max Kissel"
    address = "Munich"
    phone_number = 12345
    balance = "a"

    with pytest.raises(InvalidBalance):
        Customer.customer_signup(username, password, name, address, phone_number, balance)


def test_customer_signup_exception_invalid_balance_negative():
    username = "Max123"
    password = "Max@123"
    name = "Max Kissel"
    address = "Munich"
    phone_number = 12345
    balance = -500

    with pytest.raises(InvalidBalance):
        Customer.customer_signup(username, password, name, address, phone_number, balance)


def test_customer_signup_exception_invalid_user_exists():
    username = "Max123"
    password = "Max@123"
    name = "Max Kissel"
    address = "Munich"
    phone_number = 12345
    balance = 500

    with pytest.raises(UserExists):
        Customer.customer_signup(username, password, name, address, phone_number, balance)


def test_customer_instance_valid():

    customer_instance = Customer("Max123")

    assert customer_instance.password == "Max@12345"
    assert customer_instance.name == "Maxwell"
    assert customer_instance.address == "Hamburg"
    assert customer_instance.phone_number == 54321


def test_account_create_valid():
    username = "Shweta1"
    balance = 6000

    acct_obj_created = Account.account_create(username, balance)

    assert isinstance(acct_obj_created, Account)


def test_account_create_invalid_username():
    username = "Aaa123"
    balance = 6000

    with pytest.raises(UserNotFound):
        Account.account_create(username, balance)


def test_account_create_invalid_balance():
    username = "Shweta1"
    balance = -6000

    with pytest.raises(InvalidBalance):
        Account.account_create(username, balance)


def test_customer_login_valid():
    username = "Shweta1"
    password = "Shweta@1"
    status_expected = True

    cust_obj_login = Customer(username)
    status = cust_obj_login.login(password)

    assert status == status_expected


def test_customer_login_invalid():
    username = "Shweta1"
    password = "Shweta@123"
    status_expected = False

    cust_obj_login = Customer(username)
    status = cust_obj_login.login(password)

    assert status == status_expected


def test_account_withdraw_valid():
    """
    Tests that:
        - The account's balance after withdrawal is equal to the initial balance minus the amount withdraw.
    """
    account_withdraw = 1000000006
    withdraw_amount = 200
    account_inst_withdraw = Account(account_withdraw)
    initial_balance = account_inst_withdraw.balance
    account_inst_withdraw.withdraw(withdraw_amount)
    account_instance2 = Account(account_withdraw)

    assert account_instance2.balance == initial_balance - withdraw_amount


def test_account_withdraw_invalid_insufficient_balance():
    account_withdraw = 1000000006
    account_inst_withdraw = Account(account_withdraw)
    withdraw_amount = account_inst_withdraw.balance + 200

    with pytest.raises(InsufficientBalance):
        account_inst_withdraw.withdraw(withdraw_amount)


def test_account_deposit_valid():
    """
    Tests that:
        - The account's balance after deposit is equal to the initial balance plus the amount deposited.
    """
    account_deposit = 1000000006
    deposit_amount = 200
    account_inst_deposit = Account(account_deposit)
    initial_balance = account_inst_deposit.balance
    account_inst_deposit.deposit(deposit_amount)
    account_instance2 = Account(account_deposit)

    assert account_instance2.balance == initial_balance + deposit_amount

# def test_delete_account_valid():
#     customer_instance = Customer("Jay123")
#     list_deleted_accounts = customer_instance.delete_accounts()
#     expected_list_deleted_accounts = [1000000001,1000000002]
#
#     assert list_deleted_accounts == expected_list_deleted_accounts


