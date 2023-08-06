

def get_primeNumbers(num):
    prime_list = [1,2]
    for n in range(3, num):
        primo = True
        for i in range(2,n):
            if n % i == 0:
                primo = False
                break
        if primo:
            prime_list.append(n)
    
    return prime_list