from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from account import Account
    from loan import Loan


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
        self.accounts_list: list[Account] = []
        self.loans: list[Loan] = []
        self.profile = CustomerProfile(self)

    def update(self, account_number, old_balance, new_balance):
        print(f"Customer {self.username} was notified about of the balance change.\n\t"
              f"Balance changing for {account_number}: {old_balance} -> {new_balance}")

    def get_info(self):
        acc_list = [acc.get_info() if self.accounts_list else None for acc in self.accounts_list]
        return f"{self.username}, {self.__contact_info} " + str(acc_list)

    def add_account(self, account: 'Account'):
        if account in self.accounts_list:
            print(f"Account {account.get_info()} is already in {self.username}'s accounts list")
            return
        self.accounts_list.append(account)
        print(f"Account {account} has been successfully added.")

    def create_loan(self, amount: float, rate, term, strategy):
        loan = Loan(self, amount, rate, term, strategy)
        self.loans.append(loan)

    def remove_account(self, account: 'Account'):
        if account in self.accounts_list:
            self.accounts_list.remove(account)
        else:
            print(f"There no such account in {self.username}'s accounts list")


class CustomerProfile:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.total_balance = 0.0
        self.total_loans = 0.0
        self.credit_score = 0
        self.credit_limit = 0.0

    def evaluate_financial_status(self):
        self.total_balance = sum(acc.get_balance() for acc in self.customer.accounts_list)
        self.total_loans = sum(loan.amount for loan in self.customer.loans)
        self.calculate_credit_score()
        self.determine_credit_limit()

    def calculate_credit_score(self):
        if self.total_loans == 0:
            self.credit_score = 90 + min(self.total_balance // 1000, 10)
        else:
            ratio = self.total_balance / (self.total_loans + 1)
            self.credit_score = max(30, min(int(ratio * 10), 100))

    def determine_credit_limit(self):
        self.credit_limit = self.credit_score * 100

    def show_financial_summary(self):
        self.evaluate_financial_status()
        return (
            f"--- Financial Profile for {self.customer.username}\n"
            f"Total Balance: {self.total_balance:.2f}\n"
            f"Total Loans: {self.total_loans:.2f}\n"
            f"Credit Score: {self.credit_score}/100\n"
            f"Credit Limit: {self.credit_limit:.2f}\n"
        )
