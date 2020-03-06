n = 5
W = 10
item = [[0,0],[2,6],[5,3],[4,5],[2,4],[3,6]]
dp = []

for i in range(W+1):
    dp.append(0)
    
def printDP(l):
    print('%2d|' % l , end="")
    for i in range(0, 11):
        print('%2d ' % dp[i], end="")
    print()

def knapsack():
    for i in range(1, n + 1):
        printDP(i - 1)
        for j in range(W, item[i][0]-1, -1):
        
            dp[j] = max(dp[j], dp[j - item[i][0]] + item[i][1])


print()
print("   " , end="")
for i in range(0, 11):
    print('%2d ' % i , end="")
print()
print("   " , end="")
for i in range(0, 11):
    print("---" , end="")
print()
knapsack()
printDP(n)
print()
print(dp[W])
