import math
from random import randint
from itertools import chain, combinations
import time

def quick_pow(a, b, m):
    ab = 1
    while b > 0:
        if b & 1:
            ab = (ab * a) % m
        b >>= 1
        a = (a ** 2) % m
    return ab

def get_ds(p):
    p -= 1
    s = 0
    while p % 2 == 0:
        p >>= 1
        s += 1
    return (p, s)

def strongly_prime(p, x, d, s):
    xd = quick_pow(x, d, p)
    if xd == 1 or xd == p - 1:
        return True
    xr = xd
    for r in range(1, s):
        xr = quick_pow(xr, 2, p)
        if xr == p - 1:
            return True
        if xr == 1:
            return False

def Millera_Rabina(p):
    d, s = get_ds(p)
    if not(strongly_prime(p, 2, d, s)) or not(strongly_prime(p, 3, d, s)) or not(strongly_prime(p, 5, d, s)) or not(strongly_prime(p, 7, d, s)):
        return False
    k = 0
    while k < 5:
        x = randint(2, p - 1)
        if math.gcd(x, p) > 1 or not(strongly_prime(p, x, d, s)):
            return False
        k += 1
    return True

#

def trial_divisions(num):
    for d in range(2, int(num ** 0.5)):
        #if d >= 47:
            #break
        if num % d == 0:
            return d
    return -1

#

def f(x, num):
    return (x ** 2 + 1) % num

def Pollard(num):
    for x in range(2, num):
        y = x
        while True:
            x = f(x, num)
            y = f(f(y, num), num)
            d = math.gcd(x - y, num)
            if x == y:
                break
            if d != 1:
                return d
    return -1

#

n = 1
sn = 1
a = 1
La = 1

V = []
Al = []
A = []
U = []
B = []
B2 = []
P = {}
Fb = {}
Vec_b = {}
vec_len = 0
Vec_all = []

def calc_La():
    global La
    La = math.e ** (a * (math.log2(n) * math.log2(math.log2(n))) ** 0.5)
    print("a =", a)
    print("La =", La)

def init_Brilhart_Morrison(num):
    global n, sn, a, V, Al, A, U, B, B2, P, Fb, Vec_b, vec_len, Vec_all
    n = num
    sn = n ** 0.5
    a = (1 / 2) ** 0.5

    calc_La()

    V = [1]
    Al = [sn]
    A = [math.floor(Al[0])]
    U = [A[0]]
    B = [0, 1]
    B2 = [0, 1]
    P = {}
    Fb = {}
    Vec_b = {}
    vec_len = 0
    Vec_all = []

def table1():
    V.append((n - U[-1] ** 2) / V[-1])
    Al.append((sn + U[-1]) / V[-1])
    A.append(math.floor(Al[-1]))
    U.append(A[-1] * V[-1] - U[-1])
    #print("v =", V[-1])
    #print("al =", Al[-1])
    print("a =", A[-1])
    #print("u =", U[-1])
    
def table2():
    B.append((B[-1] * A[-1] + B[-2]) % n)
    b2 = pow(B[-1], 2, n)
    B2.append(b2 if b2 < n / 2 else b2 - n)
    print("b =", B[-1])
    print("b2 =", B2[-1])

def Legendre_symbol(a,p):
  if(a==1):
    return 1
  if(a%p==0):
    return 0
  if(a%2==0):
    return Legendre_symbol(a/2,p)*pow(-1,(pow(p,2)-1)/8)
  elif(a%2!=0 and a!=1):
    return Legendre_symbol(pow(int(p),1,int(a)),a)*pow(-1,((a-1)*(p-1))/4)

'''def Legendre_symbol(a, b):
    #return 1
    #return pow(a, int((b - 1) / 2), b)
    if a == 1:
        return 1
    if a % b == 0:
        return 0
    if a % 2 == 0:
        return Legendre_symbol(a / 2, b) * pow(-1, (pow(b, 2) - 1) / 8)
        #return Legendre_symbol(a / 2, b) * ((-1) ** ((b * b - 1) / 8))
    #return Legendre_symbol(b % a, a) * ((-1) ** ((a - 1) * (b - 1) / 4))
    return Legendre_symbol(b % a, a) * pow(-1, ((a - 1) * (b - 1)) / 4)'''

def check_divisor(p):
    #return True
    ls = Legendre_symbol(n, p)
    if ls != 1:
        print("Legendre_symbol failed", n, p)
    if p >= La:
        print("La failed")
    return ls == 1 and p < La
    #return 1

def prime_divisors(num):
    P.clear()
    if num < 0:
        P[-1] = 1
        num *= -1
        #Fb[-1] = 1
    p = 2
    while pow(p, 2) <= num:
        if num % p == 0:
            #Fb[p] = 1
            P[p] = 1
            if not check_divisor(p):
                return False
            num /= p
            while num % p == 0:
                P[p] = 1 - P[p]
                num /= p
        p += 1
    if num > 1:
        num = int(num)
        P[num] = 1
        if not check_divisor(p):
            return False
        #Fb[num] = 1
    for p in P:
        Fb[p] = 1
    print("P =", P)
    print("Fb =", list(Fb))
    return True

def build_vectors():
    print("new len =", len(Fb), "last len =", vec_len)
    append_size = len(Fb) - vec_len
    for vec in Vec_b.values():
        for i in range(append_size):
            vec.append(0)
    vec = []
    for e in Fb:
        if e in P:
            vec.append(P[e])
        else:
            vec.append(0)
    Vec_b[(B[-1], B2[-1])] = vec
    print("Vec =", Vec_b)

def power_set(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

def get_key(dictionary, value):
    for key in dictionary.keys():
        if dictionary[key] == value:
            return key

def xor_vectors(vec_a, vec_b):
    vec_c = vec_a
    for i in range(len(vec_a)):
        vec_c[i] = (vec_c[i] + vec_b[i]) % 2
    return vec_c

def solve_vectors():
    Vec_power = power_set(Vec_b.values())
    for Vecs in Vec_power:
        sum_vec = [0] * len(Fb)
        for vec in Vecs:
            sum_vec = xor_vectors(sum_vec, vec)
        if sum_vec == [0] * len(Fb):
            print("zero vector")
            X = 1
            Y = 1
            for vec in Vecs:
                b, b2 = get_key(Vec_b, vec)
                X = (X * b) % n
                Y = (Y * b2) % (n ** 2)
            Y = int(Y ** 0.5)
            if X != Y and X != n - Y:
                print("X != +- Y")
                d1 = math.gcd(X + Y, n)
                d2 = math.gcd(X - Y, n)
                if d1 != 1 and d2 != 1:
                    print(d1, d2)
                    return (d1, d2)
                print("gcd = 1")
                global a
                a += 1
            else:
                print("X = +- Y")
    return (-1, -1)

def Brilhart_Morrison(num):
    init_Brilhart_Morrison(num)
    i = 1
    while True:
        print("i =", i)
        global vec_len
        vec_len = len(Fb)
        if i != 1:
            table1()
        table2()
        i += 1
        if not prime_divisors(B2[-1]):
            continue
        build_vectors()
        res = solve_vectors()
        if res != (-1, -1):
            return res
        print()
    return (-1, -1)

#

def main_part(number):
    number_before = number
    result = []
    state = 1
    while True:
        if state % 2 == 1:
            print("stage =", state)
            if Millera_Rabina(number):
                print(number, "prime")
                result.append(number)
                break
            else:
                print(number, "not prime")
                state += 1
        if state == 2:
            print("stage =", state)
            d = trial_divisions(number)
            print("d =", d)
            if d != -1:
                result.append(d)
                state = 1
                number = int(number / d)
            else:
                state = 4
        if state == 4:
            print("stage =", state)
            d = Pollard(number)
            print("d =", d)
            if d != -1:
                result.append(d)
                state = 3
                number = int(number / d)
            else:
                state = 6
        if state == 6:
            print("stage =", state)
            d = Brilhart_Morrison(number)
            print("d =", d)
            if d != (-1, -1):
                result.append(d[0])
                state = 5
                number = int(number / d[0])
            else:
                print("povnuy kopes")
    print(result)
    res = 1
    for r in result:
        res *= r
    print(res, number_before == res)

#main_part(49347803087)

#

results = []

def measure_time(num):
    start = time.perf_counter()
    print("Pollard", Pollard(num))
    end = time.perf_counter()
    print(start, end, end - start)

values = [9172639163, 8627969789, 8937716743, 278874899, 99400891, 116381389, 4252083239, 6633776623, 227349247, 3568572617]

for r in values:
    measure_time(r)

#Brilhart_Morrison(10967535067)
