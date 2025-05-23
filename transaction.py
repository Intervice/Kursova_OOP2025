from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from account import Account
from banksystem import BankSystem


class Transaction(ABC):
    id_counter = 0

    @staticmethod
    def generate_id():
        Transaction.id_counter += 1
        return Transaction.id_counter

    def __init__(self, amount: float, account: 'Account'):
        self.transaction_id = Transaction.generate_id()
        self.account = account
        self.amount = float(amount)
        self.date = datetime.now()
        BankSystem("").add_transaction(self)

    def __del__(self):
        BankSystem("").remove_transaction(self)

    def get_info(self):
        return f"Transaction {self.transaction_id} at {self.date.strftime('%d/%m/%Y %H:%M:%S')}"

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class TransactionDeposit(Transaction):
    def __init__(self, amount, account):
        super().__init__(amount, account)

    def get_info(self):
        return super().get_info() + "\nDeposit to " + self.account.get_info() + " with amount of " + str(self.amount)

    def execute(self):
        self.account.deposit(self.amount)

    def undo(self):
        self.account.withdraw(self.amount)


class TransactionWithdraw(Transaction):
    def __init__(self, amount, account):
        super().__init__(amount, account)

    def get_info(self):
        return super().get_info() + "\nWithdraw from" + self.account.get_info() + "with amount of" + str(self.amount)

    def execute(self):
        self.account.withdraw(self.amount)

    def undo(self):
        self.account.deposit(self.amount)


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

    def undo(self):
        self.target_account.withdraw(self.amount)
        self.account.deposit(self.amount)


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
        self.undo_stack: list[Transaction] = []
        self.redo_stack: list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def batch_execute(self):
        for transaction in self.transactions:
            try:
                transaction.execute()
                self.undo_stack.append(transaction)
                self.redo_stack.clear()
                print("Done", transaction.get_info())
            except Exception as ex:
                print(f"Failed to execute transaction {transaction.transaction_id}: {ex}")
        self.transactions.clear()

    def audit_transactions(self):
        print("TRANSACTION AUDIT REPORT")
        for transaction in self.undo_stack:
            print(transaction.get_info())
        print("END OF REPORT")

    def clear_transactions(self):
        self.transactions.clear()

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        transaction = self.undo_stack.pop()
        try:
            transaction.undo()
            self.redo_stack.append(transaction)
            print(f"Undone: {transaction.get_info()}")
        except Exception as ex:
            print(f"Failed to undo transaction {transaction.transaction_id}: {ex}")

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        transaction = self.redo_stack.pop()
        try:
            transaction.execute()
            self.undo_stack.append(transaction)
            print(f"Redone: {transaction.get_info()}")
        except Exception as ex:
            print(f"Failed to redo transaction {transaction.transaction_id}: {ex}")
