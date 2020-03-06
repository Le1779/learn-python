#INF = float("inf")
#g = [[0 for x in range(11)] for y in range(11)]
#x = [0 for x in range(11)]
#bestx = [0 for x in range(100)]
#bestl = INF
#
#
#def travel(t):
#    if t > n:
#        if g[x[n], 1] != INF and (cl + g[x[n], 1]) < bestl:
#            for j in range(1, n+1):
#                bestx[j] = x[j];
#                bestl = cl + g[x[n], 1];
#    else:
#        for j in range(t, n+1):
#            if g[x[t - 1], x[j]] != INF and (cl + g[x[t - 1], x[j]]) < bestl:
#                x[t], x[j] = x[j], x[t]
#                cl = cl + g[x[t - 1], x[t]]
#                travel(t+1)
#                cl = cl - g[x[t - 1], x[t]]
#                x[t], x[j] = x[j], x[t]
#
#for i in range(1, 11):
#    for j in range(i, 11):
#        g[i][j] = g[j][i] = INF
#for i in range(11):
#    x[i] = i
#travel(2)
#print(bestl)
