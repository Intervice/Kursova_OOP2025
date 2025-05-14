from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from account import Account
    from customer import Customer
    from transaction import Transaction
    from loan import Loan

class BankSystem:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(BankSystem, cls).__new__(cls)
        return cls.__instance

    def __init__(self, title, clients_list=None, accounts_list=None, transactions_list=None, loans_list=None):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.title = title
        self.clients_list: list[Customer] = clients_list if clients_list is not None else []
        self.accounts_list: list[Account] = accounts_list if accounts_list is not None else []
        self.transactions_list: list[Transaction] = transactions_list if transactions_list is not None else []
        self.loans_list: list[Loan] = loans_list if loans_list is not None else []
        self._initialized = True

    def add_customer(self, client: 'Customer'):
        if client in self.clients_list:
            return f"Client {client} is already in the list."
        self.clients_list.append(client)
        return f"Client {client} has been successfully added."

    def remove_customer(self, client: 'Customer'):
        if client in self.clients_list:
            self.clients_list.remove(client)
            return f"Client {client}, was successfully removed."
        return f"There is no such client like {client} in client list."

    def add_account(self, account: 'Account'):
        if account not in self.accounts_list:
            self.accounts_list.append(account)
            return f"Account {account.account_number} has been successfully added."
        return f"Account {account.account_number} is already in the list."

    def remove_account(self, account: 'Account'):
        if account in self.accounts_list:
            self.accounts_list.remove(account)
            return f"Account {account.account_number}, was successfully removed."
        return f"There is no such account like {account.account_number} in account list."

    def add_loan(self, loan: 'Loan'):
        if loan not in self.loans_list:
            self.loans_list.append(loan)
            return f"Loan {loan.loan_id} has been successfully added."
        return f"Loan {loan.loan_id} is already in the list."

    def remove_loan(self, loan: 'Loan'):
        if loan in self.loans_list:
            self.loans_list.remove(loan)
            return f"Loan {loan.loan_id} was successfully removed."
        return f"There is no such loan like {loan.loan_id} in loan list."

    def add_transaction(self, transaction: 'Transaction'):
        if transaction not in self.transactions_list:
            self.transactions_list.append(transaction)
            return f"Transaction {transaction.transaction_id} has been successfully added."
        return f"Transaction {transaction.transaction_id} is already in the list."

    def remove_transaction(self, transaction: 'Transaction'):
        if transaction in self.transactions_list:
            self.transactions_list.remove(transaction)
            return f"Transaction {transaction.transaction_id} was successfully removed."
        return f"There is no such transaction like {transaction.transaction_id} in transaction list."

    def __str__(self):
        return (f"Bank System: {self.title}\n"
                f"Number of Clients: {len(self.clients_list)}\n"
                f"Number of Accounts: {len(self.accounts_list)}\n"
                f"Number of Transactions: {len(self.transactions_list)}\n"
                f"Number of Loans: {len(self.loans_list)}")
