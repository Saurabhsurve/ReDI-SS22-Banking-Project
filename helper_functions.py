import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

fh = logging.FileHandler('helper_functions.log')
fh.setFormatter(f)

logger.addHandler(fh)


# username must contain  6-12 characters and contain at least 1 alphabet and 1 number
def username_valid(username):
    valid = False
    while not valid:
        if len(username) < 6 or len(username) > 12:
            logger.debug(f'username length not valid:{username}')
            break
        elif not re.search("[a-zA-Z]", username):
            logger.debug(f'username contains no alphabet:{username}')
            break
        elif not re.search("[0-9]", username):
            logger.debug(f'username contains no number:{username}')
            break
        else:
            logger.debug(f'username valid:{username}')
            valid = True
            break
    return valid


# password must contain 6-12 characters and contain at least 1 alphabet, 1 number and 1 special character from $ # @
def password_valid(password):
    valid = False
    while not valid:
        if len(password) < 6 or len(password) > 12:
            logger.debug(f'password length not valid:{password}')
            break
        elif not re.search("[a-zA-Z]", password):
            logger.debug(f'password contains no alphabet:{password}')
            break
        elif not re.search("[0-9]", password):
            logger.debug(f'password contains no number:{password}')
            break
        elif not re.search("[$#@]", password):
            logger.debug(f'password contains no special char:{password}')
            break
        else:
            valid = True
            logger.debug(f'password valid')
            break
    return valid


def balance_valid(balance_input):
    try:
        valid = True
        balance = round(float(balance_input), 2)
        if balance < 0:
            logger.debug(f'Balance amount negative:{balance_input}')
            valid = False

    except ValueError:
        logger.debug(f'Balance amount not decimal:{balance_input}')
        valid = False
    finally:
        return valid


def append_to_csv(file_name, data):

    # Make data frame of above data
    df = pd.DataFrame(data)

    # append data frame to CSV file
    df.to_csv(file_name, mode='a', index=False, header=False)
    logger.debug(f'Data appended to csv: {file_name}')



