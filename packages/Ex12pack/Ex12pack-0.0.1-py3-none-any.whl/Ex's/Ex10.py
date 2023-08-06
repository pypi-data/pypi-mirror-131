
def fibonacci():
    fst=1
    snd=1
    yield fst
    yield snd
    while True:  
        fst = fst+snd
        snd = fst-snd
        yield fst
x=0
gen = fibonacci()
while x<10:
    x=x+1
    i = next(gen)  
    print(i)


        
