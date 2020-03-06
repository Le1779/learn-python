import time
#來源1
str1 = ['null', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A']
#來源1的長度
str1Len = len(str1)
#來源2
str2 = ['null', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'C']
#來源2的長度
str2Len = len(str2)
#長度陣列
length = [[0]*str2Len for _ in range(str1Len)]
#長度來源 0:左上（延伸長度）1:左方 2:上方
previous = [[-1]*str2Len for _ in range(str1Len)]
#LCS
lcs = []

print('length: ' + str(len(length)) + ' * ' + str(len(length[0])))

#遞迴版本
def LCS(s1, s2):
    if len(s1) == 0 or len(s2) == 0:
        return '';
    r = ''
    e1 = s1[-1]
    e2 = s2[-1]
    sub1 = list(s1)
    del sub1[-1]
    sub2 = list(s2)
    del sub2[-1]
    if e1 == e2:
        r += LCS(sub1, sub2)
        r += e1
    else:
        r1 = LCS(s1, sub2)
        r2 = LCS(sub1, s2)
        if len(r1) < len(r2):
            r += r2
        else:
            r += r1
    return r

#動態規劃版本
def getLCSLength():
    for i in range(1, str1Len):
        for j in range(1, str2Len):
            if str1[i] == str2[j]:
                length[i][j] = length[i - 1][j - 1] + 1
                previous[i][j] = 0
            else:
                if length[i - 1][j] < length[i][j - 1]:
                    length[i][j] = length[i][j - 1]
                    previous[i][j] = 1
                else:
                    length[i][j] = length[i - 1][j]
                    previous[i][j] = 2
                    
def getLCS(i, j):
    if i == 0 or j == 0:
        return
        
    if previous[i][j] == 0:
        getLCS(i - 1, j - 1)
        lcs.append(str1[i])
    elif previous[i][j] == 1:
        getLCS(i, j - 1)
    else:
        getLCS(i - 1, j)

def drawLength():
    print("     ", end ="")
    print('  '.join(str2[1:]))
    for i in range(0, str1Len):
        if i != 0:
            print(str1[i], end ="")
        else:
            print(" ", end ="")
        for j in range(0, str2Len):
            if previous[i][j] == 0:
                print("↖", end ="")
            elif previous[i][j] == 1:
                print("←", end ="")
            elif previous[i][j] == 2:
                print("↑", end ="")
            else:
                print(" ", end ="")
            print(length[i][j], end =" ")
        print()



print("")
print("-----------遞迴-----------")
tStart = time.time()
print("LCS: " + LCS(str1[1:], str2[1:]))
tEnd = time.time()
print ("Cost %f sec" % (tEnd - tStart))
print("--------------------------")
print("")

print("")
print("---------動態規劃---------")
tStart = time.time()

getLCSLength()
getLCS(str1Len - 1, str2Len - 1)
print("LCS: " + ''.join(lcs))

tEnd = time.time()
print ("Cost %f sec" % (tEnd - tStart))
print("--------------------------")
print("")
drawLength()
