def gen_number():
    gen_num = BankAccount.num_counter
    BankAccount.num_counter += 1
    return str(gen_num)


class BankAccount:
    num_counter = 5375000000000000


    def __init__(self, owner_name, balance):
        self.__account_number = gen_number()
        self.__owner_name = owner_name
        self.__balance = balance
        acc_list.append(self)

    def get_number(self):
        return self.__account_number


    def get_name(self):
        return self.__owner_name

    def deposit(self, amount):
        if isinstance(amount, (int, float)):
            if amount > 0:
                self.__balance += amount
                print("Updates balance:", self.__balance)
        else:
            print("Incorrect amount")

    def withdraw(self, amount):
        if isinstance(amount, (int, float)):
            if self.__balance >= amount > 0:
                self.__balance -= amount
                print("Updates balance:", self.__balance)
        else:
            print("Incorrect amount")


    def name_change(self, name):
        if len(name) >= 3:
            self.__owner_name = name
        else:
            print("Name is too short")


acc_list = []

def find_acc(num):
   num.replace(" ", "")
   for acc in acc_list:
       if acc.get_number() == num:
           return acc2.get_number(), acc2.get_name()
   print("Nothing were found")

acc1 = BankAccount("Ivan", 200.0)
acc2 = BankAccount("Andriy", 11500.0)

acc_list.append(acc1)
acc_list.append(acc2)

print(acc2.get_number(), acc2.get_name())
print(acc_list)

# acc2.name_change("Pe")
# acc2.deposit(200)
# acc2.withdraw("500")
# print(acc2.get_number(), acc2.get_name())
# print(find_acc("5375000000000001"))
