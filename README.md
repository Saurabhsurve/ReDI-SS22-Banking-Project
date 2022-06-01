# ReDI-SS22-Banking-Project
This is a banking project built in python as a part of intermediate python course at ReDI, Munich for Spring semester 2022.
For a visual overview of the user flow please check out the board on miro https://miro.com/app/board/uXjVOw-6_3w=/?share_link_id=339002349178
The Banking function has 2 types of users: customers and admin

Customers will be initially prompted to:
1. Login
2. Signup

On successful login the customer can perform following actions:
1. Create new Bank Account for self.
2. Request to list his/her own bank accounts
3. Request for balance
4. Withdraw amount from one of his/her account
5. Deposit amount to one of his/her own account

Admin on succesful login can perform the following actions:
1. See customer information except balance
2. Delete a customer
3. Update customer information

The customer and account data is stored in csv files

We have 3 .py files
To run the project open bank_log.py
bank_classes.py store all the class definition
helper_functions.py store all functions which are reused in multiple parts of the code
for the aboe 3 files there are corresponding log files to log debug, info and warning messages

Test cases are written in bank_test.py

The requirements.txt speciies the external modules needed for function to perform
