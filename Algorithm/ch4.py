import time

fibonacci = 40


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def fibDP(n):
    fibArray = [0]*n
    fibArray[0] = 1
    fibArray[1] = 1
    for i in range(2, n):
        fibArray[i] = fibArray[i - 2] + fibArray[i - 1]
    return fibArray[n - 1]

def fibDP2(n):
    fibArray = [0, 1]
    for i in range(2, fibonacci + 1):
        fibArray[i%2] = fibArray[0] + fibArray[1]
    return fibArray[n%2]

print("")
print("----------分治法----------")
tStart = time.time()
print(fib(fibonacci))
tEnd = time.time()
print ("Cost %f sec" % (tEnd - tStart))
print("--------------------------")
print("")

print("---------動態規劃---------")
tStart = time.time()
print(fibDP(fibonacci))
tEnd = time.time()
print ("Cost %f sec" % (tEnd - tStart))
print("--------------------------")
print("")

print("---------動態規劃2--------")
tStart = time.time()
print(fibDP2(fibonacci))
tEnd = time.time()
print ("Cost %f sec" % (tEnd - tStart))
print("--------------------------")
print("")
