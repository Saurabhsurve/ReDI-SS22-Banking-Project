import sys
import helper_functions
from bank_classes import Customer, Account, Admin
from user_defined_exceptions import InvalidUserName, InvalidPassword, InvalidBalance, UserExists, UserNotFound, \
    InvalidWithdrawAmount, InsufficientBalance, NegativeWithdrawAmount, InvalidDepositAmount, \
    NegativeDepositAmount, DuplicateUsernames, AdminNotAuthenticated
import logging
# import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

fh = logging.FileHandler('bank_login.log')
fh.setFormatter(f)

logger.addHandler(fh)


def homepage():
    logger.info('Program started: Homepage')
    print("\nWelcome to XYZ Bank")
    while True:
        try:
            print("\n1. Customer 2. Admin 3. Exit")
            choice = int(input("Who are you ?? Enter a number between 1-3: "))
            if choice not in (1, 2, 3):
                raise ValueError
            break
        except ValueError:
            print("The choice entered is invalid.")
            continue

    if choice == 1:
        homepage_customer()
    elif choice == 2:
        homepage_admin()
    elif choice == 3:
        exit_program()


def homepage_customer():
    logger.info('Customer homepage')
    print("\nWelcome to Customer Area")
    print("Choose from the below options")
    print("1. Login\n2. Signup\n3. Previous Menu\n4. Exit")
    customer_action = 0

    while True:
        try:
            customer_action = int(input("Please choose between options 1,2,3 or 4: "))
            if customer_action not in (1, 2, 3, 4):
                raise ValueError
            break
        except ValueError:
            print("The choice entered is invalid.")
            continue

    # 1. login
    if customer_action == 1:
        logger.info('Customer login page')
        # request for username and password
        print("Enter login details.")
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        try:
            cust_obj_login = Customer(username)
            status = cust_obj_login.login(password)
            if status:
                print("Login successful")
                logger.debug(f'Customer {username} logged in successfully')
                customer_actions(cust_obj_login)
            else:
                print("Password does not match")
                homepage_customer()

        except UserNotFound:
            print("Username does not exist")
            homepage_customer()

    # 2. signup
    elif customer_action == 2:
        logger.info(f'Customer signup page')
        print("Enter signup details.")

        while True:
            print("\nUsername must contain 6-12 characters with at least 1 alphabet and 1 number")
            username = input("Enter a username:")
            valid = helper_functions.username_valid(username)
            if valid:
                break
            else:
                print("Invalid username")

        while True:
            print("\nPassword must contain 6-12 characters, at least 1 alphabet, 1 number "
                  "and 1 special character from $ # @")
            password = input("Enter a password: ")
            valid = helper_functions.password_valid(password)
            if valid:
                break
            else:
                print("Invalid password")

        name = input("\nEnter your name:")
        address = input("\nEnter address:")
        phone_number = input("\nEnter a phone number:")

        while True:
            print("\nBalance amount must be a positive number")
            balance = input("Enter initial balance for your new account: ")
            valid = helper_functions.balance_valid(balance)
            if valid:
                break
            else:
                print("Invalid balance")

        try:
            cust_obj_signup = Customer.customer_signup(username, password, name, address, phone_number, balance)

            if isinstance(cust_obj_signup, Customer):
                logger.debug(f'Customer {cust_obj_signup.username} added successfully')
                print(f'Customer with username {cust_obj_signup.username} added successfully')

                try:
                    acct_obj_created = Account.account_create(username, balance)
                    if isinstance(acct_obj_created, Account):
                        logger.debug(f'Account created with account number: {acct_obj_created.account_number}')
                        print(f'Account created with account number: {acct_obj_created.account_number}')
                    else:
                        print("Account creation failed")
                except InvalidBalance:
                    print("Invalid balance.")
                except UserNotFound:
                    print("User not found")

            else:
                print("Customer creation failed")
        except InvalidUserName:
            print("Invalid username.")

        except InvalidPassword:
            print("Invalid password.")

        except InvalidBalance:
            print("Invalid balance.")

        except UserExists:
            print("Username already exists.")

        except UserNotFound:
            print("Customer creation failed")

        finally:
            homepage_customer()

    # 3. previous menu
    elif customer_action == 3:
        homepage()

    # 4. Exit
    elif customer_action == 4:
        exit_program()


def customer_actions(cust_obj_login):
    logger.info(f'Customer actions for: {cust_obj_login.username}')
    print(f'\nWelcome {cust_obj_login.name}')
    print("Choose from the below options")
    print("1. Create New Bank Account")
    print("2. List Bank Accounts(Show bank account Number with balance)")
    print("3. Show Balance")
    print("4. Withdraw")
    print("5. Deposit")
    print("6. Exit")

    customer_action = 0

    while True:
        try:
            customer_action = int(input("Please choose between options 1-:6 "))
            if customer_action not in (1, 2, 3, 4, 5, 6):
                raise ValueError
            break
        except ValueError:
            print("The choice entered is invalid.")
            continue

    # 1. Create new bank account
    if customer_action == 1:
        logger.info(f'Started create new bank account for: {cust_obj_login.username}')
        new_balance = input("What should be the balance amount in the new account? ")
        try:
            acct_obj_created = Account.account_create(cust_obj_login.username, new_balance)
            if isinstance(acct_obj_created, Account):
                logger.debug(f'Account created with account number: {acct_obj_created.account_number}')
                print(f'Account created with account number: {acct_obj_created.account_number} and balance €'
                      f'{acct_obj_created.balance:.2f}')
            else:
                print("Account creation failed")
        except InvalidBalance:
            print("Account creation failed. Invalid balance.")

        except UserNotFound:
            print("User not found.")

        finally:
            customer_actions(cust_obj_login)

    # 2. List Bank Accounts(Show bank account Number with balance
    elif customer_action == 2:
        logger.info(f'Started list bank accounts for customer: {cust_obj_login.username}')
        cust_obj_login.update_related_account_balance_dict()
        related_accounts = list(cust_obj_login.related_accounts_balance_dict.keys())
        if len(related_accounts):
            print("You have the following bank account(s):")
            for account in related_accounts:
                balance = cust_obj_login.related_accounts_balance_dict[account]
                print(f"Bank account no: {account} with balance €{balance:.2f}")
        else:
            print("You do not have any account")

        customer_actions(cust_obj_login)

    # 3. Show Balance
    elif customer_action == 3:
        logger.info(f'Started show balance for: {cust_obj_login.username}')
        cust_obj_login.update_related_account_balance_dict()
        related_accounts = list(cust_obj_login.related_accounts_balance_dict.keys())
        if len(related_accounts) == 0:
            print(f"No account in bank for username:{cust_obj_login.username}")
        elif len(related_accounts) == 1:
            account = related_accounts[0]
            balance = cust_obj_login.related_accounts_balance_dict[account]
            print(f"Bank account no: {account} with balance €{balance:.2f}")

        elif len(related_accounts) > 1:
            print("You have the following accounts:")
            for account in related_accounts:
                print(account)
            try:
                account_to_check = int(input("Enter the account number you would like to check: "))
                if account_to_check not in related_accounts:
                    raise ValueError
                else:
                    balance_in_account = cust_obj_login.related_accounts_balance_dict[account_to_check]
                    print(
                        f"Bank account no: {account_to_check} has balance €{balance_in_account:.2f}")

            except ValueError:
                print("The account number you entered is invalid.")

        else:
            print(f"You do not have any bank account.")
        customer_actions(cust_obj_login)

    # 4. Withdraw
    elif customer_action == 4:
        logger.info(f'Started withdrawal for customer: {cust_obj_login.username}')
        cust_obj_login.update_related_account_balance_dict()
        related_accounts = list(cust_obj_login.related_accounts_balance_dict.keys())

        if len(related_accounts) == 0:
            print(f"No account in bank for username:{cust_obj_login.username}")
        elif len(related_accounts) == 1:
            account = related_accounts[0]
            balance = cust_obj_login.related_accounts_balance_dict[account]
            print(f"Bank account no: {account} with balance €{balance:.2f}")
            withdraw_amount = input("Please enter the amount you want to withdraw: ")

            try:
                account_inst_withdraw = Account(account)
                account_inst_withdraw.withdraw(withdraw_amount)
                account_inst_withdraw.update_balance_in_account_database()
                account_instance2 = Account(account)
                if account_instance2.balance == account_inst_withdraw.balance:
                    print(
                        f"Withdrawal successful.Account {account} has updated balance {account_instance2.balance:.2f}")
            except InvalidWithdrawAmount:
                print("Withdrawal failed. The amount you entered is invalid")
            except InsufficientBalance:
                print(f"Withdrawal failed. Balance insufficient. The account {account} has only "
                      f"€{account_inst_withdraw.balance:.2f} ")
            except NegativeWithdrawAmount:
                print("Withdrawal failed. Withdraw amount cannot be negative")

        elif len(related_accounts) > 1:
            print("You have the following accounts:")
            for account in related_accounts:
                balance = cust_obj_login.related_accounts_balance_dict[account]
                print(f"Bank account no: {account} with balance €{balance:.2f}")

            try:
                account_withdraw = int(input("Withdraw from account number: "))
                if account_withdraw not in related_accounts:
                    raise ValueError
                else:
                    withdraw_amount = input("Please enter the amount you want to withdraw: ")
                    try:
                        account_inst_withdraw = Account(account_withdraw)
                        account_inst_withdraw.withdraw(withdraw_amount)
                        account_inst_withdraw.update_balance_in_account_database()
                        account_instance2 = Account(account_withdraw)
                        if account_instance2.balance == account_inst_withdraw.balance:
                            print(
                                f"Withdrawal successful.Account {account_withdraw} has updated balance "
                                f"{account_instance2.balance}")
                    except InvalidWithdrawAmount:
                        print("Withdrawal failed. The amount you entered is invalid")
                    except InsufficientBalance:
                        print(f"Withdrawal failed. Balance insufficient. The account {account_withdraw} has only "
                              f"€{account_inst_withdraw.balance:.2f} ")
                    except NegativeWithdrawAmount:
                        print("Withdrawal failed. Withdraw amount cannot be negative")

            except ValueError:
                print("The account number you entered is invalid.")

        else:
            print(f"You do not have any bank account.")
        customer_actions(cust_obj_login)

    # 5. Deposit
    elif customer_action == 5:
        logger.info(f'Started deposit for customer: {cust_obj_login.username}')
        cust_obj_login.update_related_account_balance_dict()
        related_accounts = list(cust_obj_login.related_accounts_balance_dict.keys())

        if len(related_accounts) == 0:
            print(f"No account in bank for username:{cust_obj_login.username}")
        elif len(related_accounts) == 1:
            account = related_accounts[0]
            balance = cust_obj_login.related_accounts_balance_dict[account]
            print(f"Bank account no: {account} with balance €{balance:.2f}")
            deposit_amount = input("Please enter the amount you want to deposit: ")

            try:
                account_inst_deposit = Account(account)
                account_inst_deposit.deposit(deposit_amount)
                account_inst_deposit.update_balance_in_account_database()
                account_instance2 = Account(account)
                if account_instance2.balance == account_inst_deposit.balance:
                    print(
                        f"Deposit successful.Account {account} has updated balance {account_instance2.balance:.2f}")
            except InvalidDepositAmount:
                print("Deposit failed. The amount you entered is invalid")

            except NegativeDepositAmount:
                print("Deposit failed. Deposit amount cannot be negative")

        elif len(related_accounts) > 1:
            print("You have the following accounts:")
            for account in related_accounts:
                balance = cust_obj_login.related_accounts_balance_dict[account]
                print(f"Bank account no: {account} with balance €{balance:.2f}")

            try:
                account_deposit = int(input("Deposit to account number: "))
                if account_deposit not in related_accounts:
                    raise ValueError
                else:
                    deposit_amount = input("Please enter the amount you want to deposit: ")
                    try:
                        account_inst_deposit = Account(account_deposit)
                        account_inst_deposit.deposit(deposit_amount)
                        account_inst_deposit.update_balance_in_account_database()
                        account_instance2 = Account(account_deposit)
                        if account_instance2.balance == account_inst_deposit.balance:
                            print(
                                f"Deposit successful.Account {account_deposit} has updated balance "
                                f"{account_instance2.balance}")
                    except InvalidDepositAmount:
                        print("Deposit failed. The amount you entered is invalid")
                    except NegativeDepositAmount:
                        print("Deposit failed. Deposit amount cannot be negative")

            except ValueError:
                print("The account number you entered is invalid.")

        else:
            print(f"You do not have any bank account.")
        customer_actions(cust_obj_login)

    # 6. Exit
    elif customer_action == 6:
        exit_program()

    else:
        print("Wrong choice.")
        customer_actions(cust_obj_login)


def homepage_admin():
    logger.info(f'Admin homepage')
    print("\nWelcome to Admin Area")
    print("Choose from the below options")
    print("1. Login\n2. Previous Menu\n3. Exit")

    admin_action = 0
    while True:
        try:
            admin_action = int(input("Please choose between options 1,2 or 3: "))
            if admin_action not in (1, 2, 3):
                raise ValueError
            break
        except ValueError:
            print("The choice entered is invalid.")
            continue

    # 1. Login
    if admin_action == 1:
        admin_login()

    # 2. Previous menu
    elif admin_action == 2:
        homepage()

    # 3. Exit
    elif admin_action == 3:
        exit_program()


def admin_login():
    # request for username and password
    logger.info(f'Admin login page')
    admin_username = input("Please enter your username: ")
    admin_password = input("Please enter your password: ")
    admin_instance = Admin(admin_username, admin_password)
    if admin_instance.authenticated:
        logger.debug(f'Admin login successful')
        print("Login successful")
        admin_actions(admin_instance)
    else:
        print("The login credentials are incorrect.")
        homepage_admin()


def admin_actions(admin_instance):
    # Should be able to see all customer information. Except the balance
    # Should be able to delete a customer.
    # Should be able to update the customer information. Except the Username

    # welcome page
    print(f'\nWelcome {admin_instance.username}')
    print("Choose from the below options")
    print("1. See customer information")
    print("2. Delete a customer")
    print("3. Update the customer information")
    print("4. Go to homepage")

    admin_action = 0
    while True:
        try:
            admin_action = int(input("Please choose between options 1-4: "))
            if admin_action not in (1, 2, 3, 4):
                raise ValueError
            break
        except ValueError:
            print("The choice entered is invalid.")
            continue

    # 1. See customer information
    if admin_action == 1:
        logger.info(f'Admin: customer information')
        customer_username = input("To check details of customer,\nenter it's username: ")
        try:
            customer_inst_admin = Customer(customer_username)
            customer_inst_admin.update_related_account_balance_dict()
            related_accounts = list(customer_inst_admin.related_accounts_balance_dict.keys())

            print("Customer information:")
            print(f"Username: {customer_inst_admin.username}")
            print(f"Password: {customer_inst_admin.password}")
            print(f"Name: {customer_inst_admin.name}")
            print(f"Address: {customer_inst_admin.address}")
            print(f"Phone number: {customer_inst_admin.phone_number}")

            if len(related_accounts) == 0:
                print("This customer has no bank account")
            elif len(related_accounts) == 1:
                print(f"Account number: {related_accounts[0]}")
            else:
                print(f"Account numbers: {related_accounts}")

        except UserNotFound:
            print(f"The customer with username {customer_username} does not exist.")

        except DuplicateUsernames:
            print(f"Error. We have more than one customer with username:{customer_username} ")

        finally:
            admin_actions(admin_instance)

    # 2. Delete a customer
    elif admin_action == 2:
        logger.info(f'Admin: customer delete')
        try:
            user_delete = input("To delete customer, enter it's username: ")
            status, accounts_deleted = admin_instance.delete_customer(user_delete)
            if status:
                print(f"Customer having username: {user_delete} deleted successfully.")
                logger.debug(f'Admin deleted customer: {user_delete}')
                if len(accounts_deleted) == 0:
                    print(f"No related accounts for this customer")
                else:
                    logger.debug(f'Admin deleted related accounts having account numbers: {accounts_deleted}')
                    print(f"Deleted related accounts having account numbers: {accounts_deleted}")
            else:
                print(f"Customer does not exist with username: {user_delete}")
        except AdminNotAuthenticated:
            print("The admin account has not been authenticated.")
        except UserNotFound:
            print(f"Customer does not exist with username: {user_delete}")
        except DuplicateUsernames:
            print("Error. More than one Customer customer with same username.")

        finally:
            admin_actions(admin_instance)

    # 3. Update the customer information
    elif admin_action == 3:
        logger.info(f'Admin: customer information update')
        username = input("Enter customer username: ")

        try:
            status = admin_instance.update_customer_info(username)
            if status:
                logger.debug(f'Admin updated customer information for :{username}')
                print(f"Customer details updated successfully.")

        except AdminNotAuthenticated:
            print("The admin account has not been authenticated.")
        except UserNotFound:
            print(f"Customer does not exist with username: {username}")
        except DuplicateUsernames:
            print("Error. More than one Customer customer with same username.")

        finally:
            admin_actions(admin_instance)

    elif admin_action == 4:
        homepage()
    else:
        admin_actions(admin_instance)


def exit_program():
    logger.info('Program ended')
    sys.exit("We are exiting the program")


if __name__ == "__main__":
    homepage()
