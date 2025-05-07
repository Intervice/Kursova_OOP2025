from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from loan import Loan
if TYPE_CHECKING:
    from account import Account


class Observer(ABC):
    @abstractmethod
    def update(self, account_number, old_balance, new_balance):
        pass

class Customer(Observer):
    id = 0

    @staticmethod
    def generate_id():
        Customer.id += 1
        return Customer.id

    def __init__(self, username: str, phone_number: str, address: str):
        self.id = Customer.generate_id()
        self.username = username
        self.__contact_info = {"phone_number": phone_number, "address": address}
        self.__accounts_list: list[Account] = []
        self.loans = []

    def update(self, account_number, old_balance, new_balance):
        print(f"Customer {self.username} was notified about of the balance change.\n\t"
              f"Balance changing for {account_number}: {old_balance} -> {new_balance}")

    def get_info(self):
        acc_list = [acc.get_info() if self.__accounts_list else None for acc in self.__accounts_list]
        return f"{self.username}, {self.__contact_info} " + str(acc_list)

    def add_account(self, account: 'Account'):
        if account in self.__accounts_list:
            print(f"Account {account.get_info()} is already in {self.username}'s accounts list")
            return
        self.__accounts_list.append(account)
        print(f"Account {account} has been successfully added.")

    def create_loan(self, amount: float, rate, term, strategy):
        loan = Loan(self, amount, rate, term, strategy)
        self.loans.append(loan)

    def remove_account(self, account: 'Account'):
        if account in self.__accounts_list:
            self.__accounts_list.remove(account)
        else:
            print(f"There no such account in {self.username}'s accounts list")
