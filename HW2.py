from abc import *
import random

########################################
#
# Name: Tyler Mertz
#
# This program imitates a banking environment with different objects types, utilizing all core concepts of OOP
#
########################################

class Person(ABC): #Abstract class that uses data abstraction to simplify the manager and teller classes
    #DOCTESTS FOR THE METHODS ACCESS AND GET_INFO WILL FAIL BECAUSE OF ID NUMBER BEING RANDOMLY GENERATED BUT THEY ARE WORKING CORRECTLY
    '''
        >>> john = Customer("john", 32)
        >>> joe = Manager("Joe")
        >>> john.openAccount("checking")
        Welcome to your Checking Account, john!
        >>> john.openAccount("savings", 500)
        Welcome to your Account, john!
        >>> joe.access(john)
        Customer Name: john | Customer Age: 32 | Customer ID: #####
        [0] | Account Type: checking account Balance: 0
        [1] | Account Type: savings account Balance: 500
        >>> joe.transfer(john, 1, 0, 50)
        50
        >>> joe.transfer(john, 1, 4, 50)
        The account you are trying to transfer with does not exist
        >>> joe.account_wipe(john, 1)
        Account deleted
        >>> joe.access(john)
        Customer Name: john | Customer Age: 32 | Customer ID: #####
        [0] | Account Type: checking account Balance: 50
        >>> john.account_list[0].deposit(3000)
        3050
        >>> joe.access(john)
        Customer Name: john | Customer Age: 32 | Customer ID: #####
        [0] | Account Type: checking account Balance: 3050
        >>> john.account_list[0].withdraw(500)
        2549
        >>> john.account_list[0].withdraw(6000)
        'Not enough funds'
        >>> ian = Customer("ian", 17)
        >>> ian.openAccount("checking")
        Welcome to your Checking Account, ian!
        >>> ian.openAccount("savings", 400)
        Sorry, you are not old enough to open a Savings Account.
        >>> john.openAccount("savings", 200)
        Sorry, you do not have enough funds to open a Savings Account
        >>> john.account_list[0].deposit(600)
        3149
        >>> randy = Teller("randy")
        >>> randy.access(john)
        Customer Name: john | Customer Age: 32 | Customer ID: #####
        >>> randy.get_info()
        'Position: Teller | Employee Name: randy |  Employee ID: ####'
        >>> joe.get_info()
        'Position: Manager | Employee Name: Joe |  Employee ID: ####'
    '''
    def __init__(self, name):
        self.name = name

    @abstractmethod #Abstract method for get_info that must be called on by subclass, not Person
    def get_info(self):
        raise NotImplementedError('Subclass implements this method')

#Manager class
class Manager(Person): #Inherits from class Person
    def __init__(self, name):
        super().__init__(name)
        self.__employee_ID = self.__createID #employee ID is encapsulated (Managers can't create their own ID)

    #creates ID for manager
    @property
    def __createID(self): #private property for creating a random number ID, Encapsulated
        return random.randint(1000, 9999)

    #access to customer information, including each account and balance
    def access(self, customer):
        print(customer.get_info)
        for i in range(len(customer.account_list)):
            print (f"[{i}] | " + str(customer.account_list[i]))

    #returns employee information
    def get_info(self): #Polymorphic between the classes customer, teller, and manager
        return f"Position: Manager | Employee Name: {self.name} |  Employee ID: {self.__employee_ID}"

    #Deletes a customers account
    def account_wipe(self, customer, accountNumber):
        if accountNumber < len(customer.account_list):
            del (customer.account_list[accountNumber])
            print ("Account deleted")
        else:
            print ("The account does not exist")

    #Lets manager transfer money in between a customers accounts
    def transfer(self, customer, account1, account2, amount):
        if type(customer) is Customer:
            if account1 < len(customer.account_list) and account2 < len(customer.account_list):
                if customer.account_list[account1].balance - amount > 0:
                    customer.account_list[account1].balance = customer.account_list[account1].balance - amount
                    customer.account_list[account2].balance = customer.account_list[account2].balance + amount
                    return customer.account_list[account2].balance
            else:
                print ("The account you are trying to transfer with does not exist")
        else:
            print ("The person identitfied is not a customer.")
# TELLER CLASS
class Teller(Person): #Inherits from class Person
    def __init__(self, name):
        super().__init__(name)
        self.__employee_ID = self.__createID  # employee ID is encapsulated (Managers can't create their own ID)

    #creates ID for teller
    @property
    def __createID(self):  #private property for creating a random number ID, Encapsulated
        return random.randint(1000, 9999)

    #Allows limited access to customer information
    def access(self, customer): #Polymorphic, more information given for manager then teller
        print(customer.get_info)

    #gets employee information
    def get_info(self):  # Polymorphic between the classes customer, teller, and manager
        return f"" \
            f"Position: Teller | Employee Name: {self.name} |  Employee ID: {self.__employee_ID}"


# CUSTOMER CLASS
class Customer(Person): #Inherits from class Person
    def __init__(self, name, age):
        super().__init__(name)
        self.__age = age
        self.account_list = []
        self.__customer_ID = self.__createID

    #Allows customer to get their own info
    @property
    def get_info(self):
        return f"Customer Name: {self.name} | Customer Age: {self.__age} | Customer ID: {self.__customer_ID}"

    #Creates ID for customer
    @property
    def __createID(self):                       #Encapsulated to prevent customer from changing ID
        return random.randint(10000, 99999)

    #Opens a saving account or checking account, checks conditions that allows person to open account
    def openAccount(self, account_Type, amount = 0):
        if account_Type == "savings":
            if  self.__age < SavingsAccount.MIN_AGE:
                print ("Sorry, you are not old enough to open a Savings Account.")
            elif amount < SavingsAccount.MIN_BALANCE:
                print ("Sorry, you do not have enough funds to open a Savings Account")
            else:
                self.account_list.append(SavingsAccount(self.name, amount))   #This append statement is an example of polymorphism
                                                                              #By modifying the account_list
        elif account_Type == "checking":
            if  self.__age < CheckingAccount.MIN_AGE:
                print ("Sorry, you are not old enough to open a Checking Account.")
            else:
                self.account_list.append(CheckingAccount(self.name))

class Account(ABC): #Account is an abstract class that is utilized by Checking and Savings account
    INTEREST = 0

    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 0

    @abstractmethod #Greeting is abstracted to reduce code comlexity
    def greeting(self):
        raise NotImplementedError('Subclass implements this method')

    #Customer can deposit into an account
    def deposit(self, amount):
        if isinstance(amount, (int, float)):
            self.balance = self.balance + amount
            return self.balance

    #Customer can withdraw from account
    def withdraw(self, amount):
        if isinstance(amount, (int,float)):
            if amount > self.balance:
                return 'Not enough funds'
            self.balance = self.balance - amount
            return self.balance
        else:
            return 'invalid operation'



class CheckingAccount(Account): #Inherits from Account
    WITHDRAW_FEE = 1
    INTEREST = 0.01
    MIN_AGE = 16

    def __init__(self, name):
        super().__init__(name)
        print(self.greeting())

    #Applies withdraw fee when customer withdraws from checking account
    def withdraw(self, amount):
        return Account.withdraw(self, amount + CheckingAccount.WITHDRAW_FEE)

    #Called when customer opens account
    def greeting(self):   #This is a polymorphism of the original greeting function in account
        return f'Welcome to your Checking Account, {self.holder}!'

    def __repr__(self):
        return f"Account Type: checking account Balance: {self.balance}"

    def __str__(self):
        return f"Account Type: checking account Balance: {self.balance}"


class SavingsAccount(Account): #Inherits from Account
    INTEREST = 0.03
    DEPOSIT_FEE = 1
    WITHDRAW_FEE = 2
    MIN_BALANCE = 250
    MIN_AGE = 18

    def __init__(self, name, balance):
        super().__init__(name)
        self.balance = balance
        print(self.greeting())

    #Called when cutomer opens Account
    def greeting(self):               #This is a polymorphism of the original greeting function in account
        return f'Welcome to your Account, {self.holder}!'

    #Subtracts deposit fee when depositing in to Savings
    def deposit(self, amount):
        return Account.deposit(self, amount - SavingsAccount.DEPOSIT_FEE)

    #Applies withdraw fee when withdrawing from savingsa
    def withdraw(self, amount):
        if self.balance - amount + SavingsAccount.WITHDRAW_FEE >= SavingsAccount.MIN_BALANCE:
            return Account.withdraw(self, amount + SavingsAccount.WITHDRAW_FEE)
        return 'min balance error'

    def __repr__(self):
        return f"Account Type: savings account Balance: {self.balance}"

    def __str__(self):
        return f"Account Type: savings account Balance: {self.balance}"