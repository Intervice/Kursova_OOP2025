from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from account import Account


class Transaction(ABC):
    id_counter = 0

    @staticmethod
    def generate_id():
        Transaction.id_counter += 1
        return Transaction.id_counter

    def __init__(self, amount: float, account: 'Account'):
        self.id = Transaction.generate_id()
        self.account = account
        self.amount = float(amount)
        self.date = datetime.now()

    def get_info(self):
        return f"Transaction {self.id} at {self.date.strftime('%d/%m/%Y %H:%M:%S')}"

    @abstractmethod
    def execute(self):
        pass


class TransactionDeposit(Transaction):
    def __init__(self, amount, account):
        super().__init__(amount, account)

    def get_info(self):
        return super().get_info() + "\nDeposit to " + self.account.get_info() + " with amount of " + str(self.amount)

    def execute(self):
        self.account.deposit(self.amount)


class TransactionWithdraw(Transaction):
    def __init__(self, amount, account):
        super().__init__(amount, account)

    def get_info(self):
        return super().get_info() + "\nWithdraw from" + self.account.get_info() + "with amount of" + str(self.amount)

    def execute(self):
        self.account.withdraw(self.amount)


class TransactionTransfer(Transaction):
    def __init__(self, amount, account, target_account):
        super().__init__(amount, account)
        self.target_account = target_account

    def get_info(self):
        return super().get_info() + (f"\nTransfer from {self.account.get_info()} to {self.target_account.get_info()} "
                                     f" with amount of {str(self.amount)}")

    def execute(self):
        self.account.withdraw(self.amount)
        try:
            self.target_account.deposit(self.amount)
        except Exception as error:
            self.account.deposit(self.amount)
            print("Error:", error)


class TransactionFactory:
    @staticmethod
    def create_transaction(operation_type: str, amount: float, account: 'Account', target_account: 'Account' = None):
        if operation_type not in ("deposit", "withdraw", "transfer"):
            raise ValueError("Incorrect operation type.")

        if operation_type == "deposit":
            return TransactionDeposit(amount, account)
        elif operation_type == "withdraw":
            return TransactionWithdraw(amount, account)
        elif operation_type == "transfer":
            if target_account is None:
                raise ValueError("Target account is required for transfer.")
            return TransactionTransfer(amount, account, target_account)


class TransactionManager:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def batch_execute(self):
        for transaction in self.transactions:
            try:
                transaction.execute()
                print("Done", transaction.get_info())
            except Exception as ex:
                print(f"Failed to execute transaction {transaction.id}: {ex}")

    def audit_transactions(self):
        print("TRANSACTION AUDIT REPORT")
        for transaction in self.transactions:
            print(transaction.get_info())
        print("END OF REPORT")

    def clear_transactions(self):
        self.transactions.clear()
