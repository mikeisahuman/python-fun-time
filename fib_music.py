##  Fibonacci Music
##  by Mike Phillips, 10/02/2019
##
##  Creating a Fibonacci sequence and using it to generate "notes" -- numbers from 1 to 7.
##  (It essentially takes the Fib. number, modulus 7.)

Nmax = 50
notes = ("A","B","C","D","E","F","G")       # for the key of A-minor

# fibonacci generator
def fib(n):
    i = 0
    num1 = 0
    num2 = 1
    while i < n:
        yield num2
        num1, num2 = num2, (num1+num2)
        i += 1

##print("\n\tFibonacci:\n")
##for q in fib(100):
##    print(q)
##print(sum(fib(100)))

##for q in fib(Nmax):
##    print( (1 + ((q-1) % 7)) )

for q in fib(Nmax):
    j = (q-1) % 7
    print(notes[j])
