import helper_functions
import pandas as pd
from user_defined_exceptions import InvalidUserName, InvalidPassword, InvalidBalance, UserExists, UserNotFound,\
    DuplicateUsernames, AccountNotFound, DuplicateAccountnumber, WrongPassword, InsufficientBalance, \
    NegativeWithdrawAmount, InvalidWithdrawAmount, NegativeDepositAmount, InvalidDepositAmount, NoRelatedAccounts,\
    AdminNotAuthenticated
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

fh = logging.FileHandler('bank_classes.log')
fh.setFormatter(f)

logger.addHandler(fh)


class Customer:
    username_list = []

    def __init__(self, username):
        logger.debug(f'Try creating customer object: {username}')
        Customer.update_username_list_from_csv()
        if username not in Customer.username_list:
            logger.debug(f'User not found: {username}')
            raise UserNotFound
        self.username = username
        self.related_accounts_balance_dict = {}
        list_dict_customer_details = self.update_customer_details_from_csv()
        if len(list_dict_customer_details) == 1:
            dict_customer_details = list_dict_customer_details[0]
            self.password = dict_customer_details["password"]
            self.name = dict_customer_details["name"]
            self.address = dict_customer_details["address"]
            self.phone_number = dict_customer_details["phone_number"]
            logger.debug(f'Customer instance created: {username}')

        else:
            logger.error(f'Duplicate users with username: {username}')
            raise DuplicateUsernames

    def delete_accounts(self):
        logger.debug(f'Delete account fn started for: {self.username}')
        self.update_related_account_balance_dict()
        related_accounts = list(self.related_accounts_balance_dict.keys())
        acc_deleted = []
        if len(related_accounts) == 0:
            logger.debug(f'No related accounts for username: {self.username}')
            return acc_deleted
        else:
            # read all accounts
            df = pd.read_csv('account_database.csv')
            # list of accounts to be deleted
            for account in related_accounts:
                acc_deleted.append(account)
            # delete related accounts
            df.drop(df.index[df['username'] == self.username], inplace=True)
            df.to_csv('account_database.csv', index=False)
            logger.debug(f'For {self.username}, deleted related accounts: {account}')
        logger.debug(f'Delete account fn finished for: {self.username}')
        return acc_deleted

    def update_related_account_balance_dict(self):
        logger.debug(f'update_related_account_balance_dict fn started for: {self.username}')
        df = pd.read_csv('account_database.csv')
        df2 = df.loc[df['username'] == self.username, ["account_number", "balance"]]
        dict_account_details = df2.set_index('account_number').to_dict()['balance']
        list_bank_accounts = dict_account_details.keys()
        for account in list_bank_accounts:
            balance = dict_account_details[account]
            self.related_accounts_balance_dict[account] = balance
        logger.debug(f'update_related_account_balance_dict fn finished for: {self.username}')

    # Update password,name,address,phone_number
    def update_customer_details_to_csv(self):
        logger.debug(f'update_customer_details_to_csv fn started for: {self.username}')
        df = pd.read_csv('customer_database.csv', index_col='username')
        df.loc[self.username, 'password'] = self.password
        df.loc[self.username, 'name'] = self.name
        df.loc[self.username, 'address'] = self.address
        df.loc[self.username, 'phone_number'] = self.phone_number
        # Write DataFrame to CSV file
        df.to_csv('customer_database.csv')
        logger.debug(f'update_customer_details_to_csv fn finished for: {self.username}')

    @classmethod
    def update_username_list_from_csv(cls):
        logger.debug(f'class fn: update_username_list_from_csv fn started')
        df = pd.read_csv('customer_database.csv')
        customer_list = df['username'].to_list()
        for username_item in customer_list:
            Customer.username_list.append(username_item)
        logger.debug(f'class fn: update_username_list_from_csv fn finished')

    def update_customer_details_from_csv(self):
        logger.debug(f'update_customer_details_from_csv fn started for {self.username}')
        df = pd.read_csv('customer_database.csv')
        df2 = df.loc[df['username'] == self.username, ["username", "password", "name", "address", "phone_number"]]
        list_dict_customer_details = df2.to_dict('records')
        logger.debug(f'update_customer_details_from_csv fn completed for {self.username}')
        return list_dict_customer_details

    def login(self, password):
        if self.password != password:
            logger.debug(f'Customer login failed: {self.username}')
            return False
        else:
            logger.debug(f'Customer login success: {self.username}')
            return True

    @classmethod
    def customer_signup(cls, username, password, name, address, phone_number, balance):
        username_valid = helper_functions.username_valid(username)
        if not username_valid:
            raise InvalidUserName

        password_valid = helper_functions.password_valid(password)
        if not password_valid:
            raise InvalidPassword

        # balance convert to float
        balance_valid = helper_functions.balance_valid(balance)
        if not balance_valid:
            raise InvalidBalance

        Customer.update_username_list_from_csv()
        if username in Customer.username_list:
            logger.debug(f'Signup failed: user exists: {username}')
            raise UserExists

        # if no errors write user to database
        data_customer = {
            'username': [username],
            'password': [password],
            'name': [name],
            'address': [address],
            'phone_number': [phone_number]
        }

        # write the new account and customer data to csv files
        helper_functions.append_to_csv('customer_database.csv', data_customer)

        # update customer list from csv
        Customer.update_username_list_from_csv()

        # fetch object from database
        cust_obj_signup = Customer(username)
        logger.debug(f'Customer signup success: {username}')
        return cust_obj_signup


class Account:
    account_list = []
    # Starting account number, account number is 10 digit
    STARTING_ACCOUNT_NUMBER = 1000000000

    def __init__(self, account_number):
        logger.debug(f'Try to create account instance: {account_number}')
        Account.update_account_list_from_csv()
        if account_number not in Account.account_list:
            logger.debug(f'Account not found: {account_number}')
            raise AccountNotFound
        self.account_number = int(account_number)
        list_dict_account_details = self.update_account_details_from_csv()
        if len(list_dict_account_details) == 1:
            dict_customer_details = list_dict_account_details[0]
            self.username = dict_customer_details["username"]
            self.balance = dict_customer_details["balance"]
        else:
            logger.error(f'Duplicate account number: {account_number}')
            raise DuplicateAccountnumber

    @classmethod
    def account_create(cls, username, balance):
        balance_valid = helper_functions.balance_valid(balance)
        if not balance_valid:
            raise InvalidBalance

        balance_float = round(float(balance), 2)

        Customer.update_username_list_from_csv()
        if username not in Customer.username_list:
            raise UserNotFound

        # Get new account number
        Account.update_account_list_from_csv()
        if len(Account.account_list) == 0:
            new_account_number = Account.STARTING_ACCOUNT_NUMBER
        else:
            last_account_number = max(Account.account_list)
            new_account_number = last_account_number + 1

        # if no errors write account to database
        data_account = {
            'account_number': [new_account_number],
            'username': [username],
            'balance': [balance_float]
        }

        # write the new account and customer data to csv files
        helper_functions.append_to_csv('account_database.csv', data_account)

        # update account list from csv
        Account.update_account_list_from_csv()

        # fetch object from database
        acct_obj_created = Account(new_account_number)

        return acct_obj_created

    @classmethod
    def update_account_list_from_csv(cls):
        df = pd.read_csv('account_database.csv')
        account_list = df['account_number'].to_list()
        for account_number_item in account_list:
            Account.account_list.append(account_number_item)

    def update_account_details_from_csv(self):
        df = pd.read_csv('account_database.csv')
        df2 = df.loc[df['account_number'] == self.account_number, ["account_number", "username", "balance"]]
        list_dict_account_details = df2.to_dict('records')
        return list_dict_account_details

    def withdraw(self, withdraw_amount):
        logger.debug(f'Withdraw fn started for account {self.account_number}')
        try:
            withdraw_float = round(float(withdraw_amount), 2)
            if withdraw_float < 0:
                logger.debug(f'Withdraw amount negative')
                raise NegativeWithdrawAmount
            elif self.balance < withdraw_float:
                raise InsufficientBalance
            else:
                self.balance -= withdraw_float
                self.update_balance_in_account_database()
                logger.debug(f'Withdrawal successful for account: {self.account_number}')
        except ValueError:
            logger.debug(f'Withdraw amount invalid')
            raise InvalidWithdrawAmount

    def deposit(self, deposit_amount):
        logger.debug(f'Deposit fn started for account {self.account_number}')
        try:
            deposit_float = round(float(deposit_amount), 2)
            if deposit_float < 0:
                logger.debug(f'Deposit amount negative')
                raise NegativeDepositAmount
            else:
                self.balance += deposit_float
                self.update_balance_in_account_database()
                logger.debug(f'Deposit successful for account: {self.account_number}')
        except ValueError:
            logger.debug(f'Deposit amount invalid')
            raise InvalidDepositAmount

    def update_balance_in_account_database(self):
        df = pd.read_csv('account_database.csv', index_col='account_number')
        df.loc[self.account_number, 'balance'] = self.balance
        # Write DataFrame to CSV file
        df.to_csv('account_database.csv')
        logger.debug(f'Balance updated for account:{self.account_number}')


class Admin:
    # admin login credentials
    USERNAME = 'admin'
    PASSWORD = 'pass@123'

    def __init__(self, username, password):
        self.username = Admin.USERNAME
        self.password = Admin.PASSWORD

        if self.username == username and self.password == password:
            logger.debug(f'admin authenticate successful')
            self.authenticated = True
        else:
            logger.debug(f'admin authenticate failed')
            self.authenticated = False

    def delete_customer(self, username):
        if not self.authenticated:
            raise AdminNotAuthenticated
        customer_instance_delete = Customer(username)
        # delete related accounts
        accounts_deleted = customer_instance_delete.delete_accounts()

        # delete customer from database
        df = pd.read_csv('customer_database.csv')
        df.drop(df.index[df['username'] == username], inplace=True)
        df.to_csv('customer_database.csv', index=False)
        logger.debug(f'Customer delete successful: {username}')
        return True, accounts_deleted

    def update_customer_info(self, username):
        status = False
        if not self.authenticated:
            raise AdminNotAuthenticated
        customer_instance_update = Customer(username)

        while True:
            try:
                print(f'\nChoose the field to modify for username: {customer_instance_update.username} '
                      ' \n1.Password\n2.Name\n3.Address\n4.Phone number\n5.Save and Exit')
                field = int(input("Please enter your choice from 1-5: "))
                if field < 1 or field > 5:
                    raise ValueError

            except ValueError:
                print("Option entered is invalid. You can choose a number between 1 to 5.")

            if field == 1:
                while True:
                    password_entered = input("enter new password: ")
                    valid = helper_functions.password_valid(password_entered)
                    if valid:
                        customer_instance_update.password = password_entered
                        break
                    else:
                        print("password must have 6-12 char at least 1 alphabet, number and "
                              "special character [$ # @]")

            elif field == 2:
                customer_instance_update.name = input("enter new name: ")

            elif field == 3:
                customer_instance_update.address = input("enter new address: ")

            elif field == 4:
                customer_instance_update.phone_number = input("enter new phone number: ")

            elif field == 5:
                break

        # Write DataFrame to CSV file
        customer_instance_update.update_customer_details_to_csv()
        try:
            customer_modified = Customer(username)
            if isinstance(customer_modified, Customer):
                status = True
                logger.debug(f'Customer details updated successfully')
        except UserNotFound:
            # status stays false
            logger.error(f'Unexpected error. Customer details not updated, UserNotFound')
            print("Unexpected error. Customer details not updated")
        except DuplicateUsernames:
            #  status stays false
            logger.error(f'Unexpected error. Customer details not updated, DuplicateUsernames')
            print("Unexpected error. Customer details not updated")

        finally:
            return status










