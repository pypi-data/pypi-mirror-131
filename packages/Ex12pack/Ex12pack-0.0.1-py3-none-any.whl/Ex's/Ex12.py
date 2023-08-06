

class student:
    def __init__(self, name, age, avg1):
        self.name = name
        self.age = age
        self.avg1 = avg1

    @property
    def avg(self):
        return self.avg1

    @avg.setter
    def avg(self, value):
        self.avg1 = value

    def __str__(self):
        return 'name: {self.name}, age: {self.age}, avg: {self.avg}'.format(self=self)
        

class teacher:
    def __init__(self, name, age, salary):
        self.name=name
        self.age=age
        self.salary=salary
    def __repr__(self):
        return 'name: {self.name}, age: {self.age}, salary: {self.salary}'.format(self=self)

# oenry = student("henry", "12", "69")
# print(oenry)
# oenry.avg = "23"
# print(oenry)
# genry = teacher("genry", "35", "1200")
# print(genry)