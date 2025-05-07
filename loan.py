from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from datetime import datetime
if TYPE_CHECKING:
    from customer import Customer


class InterestStrategy(ABC):
    @abstractmethod
    def calculate_percentage(self, amount: float, rate: float, term: int) -> float:
        pass


class SimpleInterest(InterestStrategy):
    def calculate_percentage(self, amount: float, rate: float, term: int) -> float:
        return amount * rate * term


class CompoundInterest(InterestStrategy):
    def calculate_percentage(self, amount: float, rate: float, term: int) -> float:
        return amount * ((1 + rate) ** term - 1)


class Loan:
    loan_id = 0

    @staticmethod
    def generate_id():
        Loan.loan_id += 1
        return Loan.loan_id

    def __init__(self, client: 'Customer', amount: float, interest_rate: float, term: int,
                 interest_strategy: InterestStrategy, status: str = "issued"):

        if status not in ("issued", "redeemed"):
            raise ValueError("Wrong loan status given. It must be 'issued' or 'redeemed'.")

        self.id = Loan.generate_id()
        self.client = client
        self.amount = float(amount)
        self.interest_rate = float(interest_rate)
        self.term = term
        self.interest_strategy = interest_strategy
        self.status = status
        self.date_created = datetime.now()

    def calculate_interest(self) -> float:
        return self.interest_strategy.calculate_percentage(self.amount, self.interest_rate, self.term)

    def change_status(self, new_status: str):
        if new_status not in ("issued", "redeemed"):
            raise ValueError("Status must be 'issued' or 'redeemed'.")
        # Думав зробити випадок, якщо статус_новий == статус_старий
        self.status = new_status

    def get_info(self) -> str:
        return (f"Loan ID: {self.id}\n"
                f"Client: {self.client.username}\n"
                f"Amount: {self.amount}\n"
                f"Rate: {self.interest_rate}\n"
                f"Term: {self.term}\n"
                f"Status: {self.status}\n"
                f"Date Created: {self.date_created.strftime('%d/%m/%Y')}\n"
                f"Interest: {self.calculate_interest():.2f}")
