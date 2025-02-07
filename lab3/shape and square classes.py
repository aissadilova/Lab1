class Shape:
    def area(self):
        return 0
class Square(Shape):
    def __init__(self, lngt=0):
        self.lngt = lngt
    def print_area(self):
        self.area = self.lngt ** 2
        print('Area of square: ', self.area)
    def get_lngt(self):
        self.lngt = int(input('Lenght of square: '))
class Rectangle(Shape):
    def __init__(self, lngt=0, wdth=0):
        self.lngt = lngt
        self.wdth = wdth
    def print_area(self):
        self.area = self.lngt * self.wdth
        print('Area of rectagle; ', self.area)
    def get(self):
        self.lngt = int(input('Langth of trectangle: '))
        self.wdth = int(input('Width of trectangle: '))

sq = Square()
sq.get_lngt()
sq.print_area()

rct = Rectangle()
rct.get()
rct.print_area()
