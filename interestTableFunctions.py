#helper functions
def __sanitize_rate(rate):
    if type(rate) == str:
        if "%" in rate: 
            return float(rate.split("%")[0].strip())/100
        else:
            return float(rate)
    else:
        return rate

def effectiveInterestConverter(interest = 0, old = 1, new = 1):
    #ratio between old and new interest rate
    return interest **(new/old)

#A series
def FP(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return (1+i)**n
def PF(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return (1+i)**-n
def FA(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return ((1+i)**n-1)/i
def PA(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return ((1+i)**n-1)/(i*(1+i)**n)
def AF(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return FA(i,n)**-1
def AP(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return PA(i,n)**-1

#G series
def PG(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return (1/i)*(((1+i)**n-1)/(i*(1+i)**n) - (n/(1+i)**n))
def AG(rate,n,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return 1/i - n/((1+i)**n-1)

#Geometric Series
def PGEO(rate,n,f,when=0):
    i = __sanitize_rate(rate)
    n = (n-1 if when == 1 else n)
    return 1/(i-f) * (1-PF(i,n)*FP(f,n))