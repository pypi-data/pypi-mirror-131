def logged (func):
    def init(*ints):
        print("this is the numbers that went into the func: " + str(ints))
        print("they retruned: " + str(func(*ints)))
        print(str(func(*ints)))
    return  init


@logged
def add(*ints):
    
    sum = 0
    for n in ints:
        sum = sum + n
    return sum

add(2,4,5)