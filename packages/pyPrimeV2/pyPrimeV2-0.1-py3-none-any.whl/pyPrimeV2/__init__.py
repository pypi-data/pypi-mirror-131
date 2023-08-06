""" 
This function receives an integer 'n' as argument and returns an array 
with the prime numbers between 1 and n (n inclusive).
"""

def n_prime(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, num):
            if(num % i == 0):
                is_prime = False
                break
        if(is_prime):
            primes.append(num)
    return primes