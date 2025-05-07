from datetime import datetime
from typing import List, TYPE_CHECKING
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from account import Account
    from transaction import Transaction


class Report(ABC):
    def __init__(self, start_date: datetime, end_date: datetime):
        if start_date > end_date:
            raise ValueError("Start date must be before end date.")
        self.start_date = start_date
        self.end_date = end_date

    @abstractmethod
    def generate(self, data) -> str:
        pass


class TransactionReport(Report):
    def generate(self, transactions: List['Transaction']) -> str:
        report = f"--- Transactions Report ---\n"
        report += f"Period: {self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}\n"
        filtered = [
            t for t in transactions
            if self.start_date <= t.date <= self.end_date
        ]
        for t in filtered:
            report += t.get_info() + "\n"
        return report if filtered else report + "No transactions found.\n"


class AccountReport(Report):
    def generate(self, accounts: List['Account']) -> str:
        report = f"--- Accounts Report ---\n"
        report += f"Period: {self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}\n"
        for acc in accounts:
            report += acc.get_info() + "\n"
        return report if accounts else report + "No accounts found.\n"


class ReportFactory:
    @staticmethod
    def create_report(report_type: str, start_date: datetime, end_date: datetime) -> Report:
        if report_type == "transactions":
            return TransactionReport(start_date, end_date)
        elif report_type == "accounts":
            return AccountReport(start_date, end_date)
        else:
            raise ValueError("Invalid report type. Must be 'transactions' or 'accounts'")
