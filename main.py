import math

n = 25511
sn = n ** 0.5

# init
V = [1]
Al = [sn]
A = [math.floor(Al[0])]
U = [A[0]]
B = [0, 1]
B2 = [0, 1]
Fb = set()

def table1():
    V.append((n - U[-1] ** 2) / V[-1])
    Al.append((sn + U[-1]) / V[-1])
    A.append(math.floor(Al[-1]))
    U.append(A[-1] * V[-1] - U[-1])
    #print("v =", V[-1])
    #print("al =", Al[-1])
    print("a =", A[-1])
    #print("u =", U[-1])
    print()
    
def table2():
    B.append(B[-1] * A[-1] + B[-2])
    b2 = pow(B[-1], 2, n)
    B2.append(b2 if b2 < n / 2 else b2 - n)
    print("b =", B[-1])
    print("b2 =", B2[-1])
    print()

def prime_divisors(num):
    P = {}
    if num < 0:
        P[-1] = 1
        num *= -1
        Fb.add(-1)
    p = 2
    while pow(p, 2) <= num:
        if num % p == 0:
            Fb.add(p)
            P[p] = 1
            num /= p
            while num % p == 0:
                P[p] = (P[p] + 1) % 2
                num /= p
        p += 1
    if num > 1:
        P[int(num)] = 1
        Fb.add(int(num))
    print("p =", P)
    #[Fb].sort()
    print("Fb =", Fb)
    return P

def Brilhart_Morrison():
    i = 0
    for i in range(10):
        #print("i =", i + 1)
        if i != 0:
            table1()
        table2()
        prime_divisors(B2[-1])
        #build_vectors()

Brilhart_Morrison()
#prime_divisors(18412)

#concat(add, sum) hash maps
#all combinations of vectors
