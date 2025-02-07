class Account:
    def __init__(self, owner, balance=0):
        """Создает банковский счет с владельцем и начальным балансом"""
        self.owner = owner
        self.balance = balance
    
    def deposit(self):
        """Позволяет пользователю пополнить баланс"""
        amount = float(input("Введите сумму для пополнения: "))
        self.balance += amount
        print(f"Пополнено {amount}. Новый баланс: {self.balance}")
    
    def withdraw(self):
        """Позволяет пользователю снять деньги, но не больше доступного баланса"""
        amount = float(input("Введите сумму для снятия: "))
        if amount > self.balance:
            print("Ошибка: недостаточно средств!")
        else:
            self.balance -= amount
            print(f"Снято {amount}. Новый баланс: {self.balance}")
    
    def show_balance(self):
        """Выводит текущий баланс"""
        print(f"Текущий баланс: {self.balance}")

# Основной код работы программы
owner_name = input("Введите имя владельца счета: ")
account = Account(owner_name)

while True:
    action = input("Выберите действие (deposit/withdraw/balance/exit): ").lower()
    if action == "deposit":
        account.deposit()
    elif action == "withdraw":
        account.withdraw()
    elif action == "balance":
        account.show_balance()
    elif action == "exit":
        print("Выход из системы.")
        break
    else:
        print("Некорректная команда. Попробуйте снова.")