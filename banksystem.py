from customer import Customer

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
        self.clients_list = clients_list if clients_list is not None else []
        self.accounts_list = accounts_list if accounts_list is not None else []
        self.transactions_list = transactions_list if transactions_list is not None else []
        self.loans_list = loans_list if loans_list is not None else []

    def add_client(self, client: Customer):
        if client in self.clients_list:
            return f"Client {client} is already in the list."
        self.clients_list.append(client)
        return f"Client {client} has been successfully added."

    def remove_client(self, client: Customer):
        if client in self.clients_list:
            self.clients_list.remove(client)
            return f"Client {client}, was successfully removed."
        return f"There is no such client like {client} in client list."
