
with open("JIS0201", "rb") as f:
    list = []
    byte = f.read(1)
    while byte:
        list.append(byte)
        byte = f.read(1)
    #print(list)

print(len(list))
result = ""
for h in range(16):
    for w in range(16):
        index = 39*32 + int(w/8) + h*2
        ret = (int.from_bytes(list[index], "big") & (0x80 >> (w % 8))) > 0
        result += "@" if ret else "_"
        if (ret):
            print(int.from_bytes(list[index], "big"))
            print(bin(int.from_bytes(list[index], "big")))
    result += '\n'
print(result)
print(bin(0x80 >> (9 % 8)))

#用一個byte代表一個點 如果是16 pixel 則需要16/8 = 2 bytes的空間來敘述一行
#如果每行需要2bytes來描述 一個字則需要 16*2 = 32bytes的空間來描述

height = 16
width = 16
rowBytes = int(16/8)
fontSpace = height*rowBytes
position = 39

for h in range(height):
    for w in range(rowBytes):
        index = position*fontSpace + h*rowBytes + w
        
