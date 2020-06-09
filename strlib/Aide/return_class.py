
from math import radians, asin, tan

class int_choice_index(int):
    def __new__(cls, value1, value2, index):
        print("value1: ", value1)
        print("value2: ", value2)
        print("index: ", index)
        return super(int_choice_index, cls).__new__(cls, value2)
    def __init__(self, value1, value2, index):
        super().__init__()
        self.index = index
    def __iter__(self):
        return iter((self, self.index))


class float_choice_index(float):
    def __new__(cls, value, index):
        return super(float_choice_index, cls).__new__(cls, value)
    def __init__(self, value, index):
        super().__init__()
        self.index = index
    def __iter__(self):
        return iter((self, self.index))


class str_choice_index(str):
    def __new__(cls, value, index):
        return super(str_choice_index, cls).__new__(cls, value)
    def __init__(self, value, index):
        super().__init__()
        self.index = index
    def __iter__(self):
        return iter((self, self.index))

if __name__ == "__main__":

    a, b = test(6,2,352,4)
    print(a)
    #print(c)

