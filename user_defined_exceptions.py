# User defined exceptions

class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidUserName(Error):
    """Username is invalid"""
    pass


class InvalidPassword(Error):
    """Password is invalid"""
    pass


class InvalidBalance(Error):
    """Balance is invalid"""
    pass


class UserExists(Error):
    """User exists in database"""
    pass


class UserNotFound(Error):
    """User not found in database"""
    pass


class WrongPassword(Error):
    """Password does not match"""
    pass


class AccountNotFound(Error):
    """Account not found in database"""
    pass


class DuplicateUsernames(Error):
    """Duplicate usernames found in database"""
    pass


class DuplicateAccountnumber(Error):
    """Duplicate account numbers found in database"""
    pass


class InvalidChoice(Error):
    """The choice value is invalid"""
    pass


class BalanceInsufficient(Error):
    """Insufficient balance in the account"""
    pass


class NoAccount(Error):
    """You do not have account"""
    pass


class NegativeNumber(Error):
    """Amount entered is negative"""
    pass


class InsufficientBalance(Error):
    """Insufficient balance"""
    pass


class NegativeWithdrawAmount(Error):
    """Withdraw amount cannot be negative"""
    pass


class InvalidWithdrawAmount(Error):
    """Withdraw amount is invalid"""
    pass


class InvalidDepositAmount(Error):
    """Deposit amount is invalid"""
    pass


class NegativeDepositAmount(Error):
    """Deposit amount cannot be negative"""
    pass


class NoRelatedAccounts(Error):
    """No related accounts for this customer"""
    pass


class AdminNotAuthenticated(Error):
    """ Admin not authenticated """
