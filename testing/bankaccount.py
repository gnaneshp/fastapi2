class BankAccount:
    def __init__(self,balance=0):
        self.balance=balance
    def withdraw(self,amount):
        if amount>self.balance:
            raise Exception("Insufficient Balance")
        self.balance-=amount
    def deposit(self,amount):
        self.balance+=amount
    def collect_interest(self):
        self.balance*=1.1


    