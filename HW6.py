# Assignment 6: Object-Oriented Programming
# Nazanin Hoseini

def validate_amount(amount):
    return amount > 0

class BankAccount:
    bank_name = "First National Bank"
    
    def __init__(self, account_holder: str, initial_balance):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if validate_amount(amount):  # بدون self. چون تابع بیرون کلاس تعریف شده
            self.balance += amount
            self.transactions.append(f"Deposit: +${amount}")
            print(f"${amount} deposited. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if not validate_amount(amount):
            print("Invalid withdrawal amount")
        elif amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount}")
            print(f"${amount} withdrawn. New balance: ${self.balance}")

    def __str__(self):
        return f"Account Holder: {self.account_holder}, Balance: ${self.balance}"

    def change_bank_name(self, new_name):
        BankAccount.bank_name = new_name  # چون دیگه cls نداریم، مستقیم به کلاس ارجاع دادم

    def show_transactions(self):
        print("Transaction History:")
        for x in self.transactions:
            print(x)


class SavingsAccount(BankAccount):
    def __init__(self, account_holder, initial_balance, interest_rate):
        super().__init__(account_holder, initial_balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)

    def __str__(self):
        return f"Savings Account - Account Holder: {self.account_holder}, Balance: ${self.balance}, Interest Rate: {self.interest_rate * 100}%"



print("\n=== Task 7 Test ===")
savings = SavingsAccount("Nznin", 1000, 0.05)
savings.deposit(50)
savings.add_interest()
print(savings)