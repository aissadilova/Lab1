class StringManipulator:
   def__init__(self):
        self.text = ""

    def getString(self):
        while True:
            self.text = input("Введите строку: ").strip()
            if self.text:
                break
            print("Ошибка: строка не может быть пустой!")

    def printString(self):
        if self.text:
            print("Результат:", self.text.upper())
        else:
            print("Ошибка: сначала введите строку с помощью getString()!")

# Использование
if __name__ == "__main__":
    obj = StringManipulator()
    obj.getString()
    obj.printString()
