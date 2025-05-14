from account import AccountFactory
from customer import Customer
from loan import SimpleInterest
from report import ReportFactory
from banksystem import BankSystem
from datetime import datetime
import time
from transaction import TransactionFactory

if __name__ == "__main__":
    bank = BankSystem("MONOBAK")

    acc1 = AccountFactory.create_account("current")
    cus1 = Customer("Intervice","321312312", "Tysmenytsya")
    print(acc1.get_info())
    acc1.attach_owner(cus1)
    print("Balance ->", acc1.get_balance())
    acc1.deposit(200)
    acc1.withdraw(103)

    print("\n\n", cus1.profile.show_financial_summary())
    cus1.create_loan(105.5, 0.5, 12, SimpleInterest(), "issued")
    print(cus1.profile.show_financial_summary())

    t1 = datetime.now()
    time.sleep(2)
    t2 = datetime.now()

    acc_report = ReportFactory.create_report("accounts", t1, t2)
    result = acc_report.generate([acc1])
    print(result)

    tf = TransactionFactory.create_transaction("deposit", 250.0, acc1)
    tf.execute()

    cus1.remove_account(acc1)
    print("After removing account from customer acc_list\n", acc1.get_info())

