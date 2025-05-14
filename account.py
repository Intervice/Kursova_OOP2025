from typing import TYPE_CHECKING
from banksystem import BankSystem
if TYPE_CHECKING:
    from customer import Customer

class Account:
    account_number = 5375000000000000

    @staticmethod
    def generate_acc_number():
        Account.account_number += 1
        return str(Account.account_number)

    def __init__(self, type_of_account):
        self.__account_number = Account.generate_acc_number()
        self.__balance = 0.0
        self.__type_of_account = type_of_account
        self.__owner = None
        BankSystem("").add_account(self)


    def attach_owner(self, customer: 'Customer'):
        self.__owner = customer
        if self not in customer.accounts_list:
            customer.accounts_list.append(self)

    def detach_owner(self):
        if self in self.__owner.accounts_list:
            self.__owner.accounts_list.remove(self)
        self.__owner = None

    def notify(self, old_balance):
        if self.__owner:
            self.__owner.update(self.__account_number, old_balance, self.__balance)
        else:
            print("This account have no customer")

    def get_balance(self):
        return self.__balance

    def get_info(self):
        return f"{self.__owner.username if self.__owner else ''} {self.__account_number} -> {self.__balance}"

    def get_owner(self):
        return self.__owner

    @staticmethod
    def check_balance_amount(amount):
        try:
            amount = int(amount)
            if amount > 0:
                return True
            print("Amount value can't be negative.")
        except ValueError:
            print("Amount value it's not a number.")
        else:
            print("Something went wrong.")

    def deposit(self, amount):
        if Account.check_balance_amount(amount):
            old_balance = self.__balance
            self.__balance += amount
            self.notify(old_balance)

    def withdraw(self, amount):
        if Account.check_balance_amount(amount):
            if self.__balance >= amount:
                old_balance = self.__balance
                self.__balance -= amount
                self.notify(old_balance)
            else:
                raise ValueError("There is no enough money to withdraw.")

    def __del__(self):
        BankSystem("").remove_account(self)

class CurrentAccount(Account):
    def __init__(self):
        super().__init__("current")


class SavingsAccount(Account):
    def __init__(self):
        super().__init__("savings")


class AccountFactory:
    acc_type = ("current", "savings")

    @staticmethod
    def create_account(account_type):
        if account_type == AccountFactory.acc_type[0]:
            return CurrentAccount()
        elif account_type == AccountFactory.acc_type[1]:
            return SavingsAccount()
        else:
            raise ValueError("Wrong account type was given.")
