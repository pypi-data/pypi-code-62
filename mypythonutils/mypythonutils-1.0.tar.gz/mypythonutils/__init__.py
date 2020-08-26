def showlist(L, mode):
    if mode == "horizontal":
        end = " "
    elif mode == "vertical":
        end = "\n"
    else:
        end = mode
    
    for i in range(len(L)-1):
        print(L[i], end = end)
    print(L[-1])
    
    return

def squareroot(num):
    return(num ** 0.5)

def listprimes(max):
    L = []
    if max == 2:
        L.append(2)
        return(L)
    for i in range(2, max +1 ):
        isprime = True

        for j in range(2,int(i ** 0.5) + 1):
            if i % j == 0:
                isprime = False
                break
        
        if isprime == True:
            L.append(i)
    
    return(L)
