class Person:
    def __init__(self, name):
        self.name = name
        self.count = None
        self.age = list()
        self.height = list()
        self.weight = list()
        self.average_age = None
        self.average_height = None
        self.average_weight = None
        self.get_info()
        self.set_average_age()
        self.set_average_height()
        self.set_average_weight()

    def get_info(self):
        self.count = int(input())

        self.age = list(map(float, input().split(" ")))
        self.height = list(map(float, input().split(" ")))
        self.weight = list(map(float, input().split(" ")))

    def set_average_age(self):
        self.average_age = sum(self.age) / self.count

    def set_average_height(self):
        self.average_height = sum(self.height) / self.count

    def set_average_weight(self):
        self.average_weight = sum(self.weight) / self.count

    def compare(self, other):
        if self.average_height > other.average_height:
            return self.name
        elif self.average_height < other.average_height:
            return other.name
        else:
            if self.average_weight < other.average_weight:
                return self.name
            elif self.average_weight > other.average_weight:
                return other.name
            else:
                return "Same"

    def get_average_age(self):
        return self.average_age

    def get_average_height(self):
        return self.average_height

    def get_average_weight(self):
        return self.average_weight


a = Person("A")
b = Person("B")
print(a.get_average_age())
print(a.get_average_height())
print(a.get_average_weight())
print(b.get_average_age())
print(b.get_average_height())
print(b.get_average_weight())
print(a.compare(b))


