guess = 20

for num in range(1, 100):
    if num == guess:
        print (num)

minNum = 0
maxNum = 100

while minNum <= maxNum:
    midNum = (minNum + maxNum)//2
    if midNum > guess:
        maxNum = midNum - 1
    elif midNum < guess:
        minNum = midNum + 1
    else:
        break
print(midNum)

fibonacci = 20

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(fibonacci))

#空間換取時間
fibArray = [0, 1]
for i in range(2, fibonacci + 1):
    fibArray[i%2] = fibArray[0] + fibArray[1]

print(fibArray[fibonacci%2])

for(int i = 1; i <= n; i *= 2){
    for(int j = 1; j <=i; j++){
        do somting
    }
}