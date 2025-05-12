from account import AccountFactory
from customer import Customer


acc1 = AccountFactory.create_account("current")
cus1 = Customer("Intervice","321312312", "Tysmenytsya")
acc1.attach_owner(cus1)

print(acc1.get_balance())
acc1.deposit(200)
acc1.withdraw(103)

