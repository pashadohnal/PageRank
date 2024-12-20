import random as rn
import networkx as nx
import numpy as np

#Written in collaboration with Wiktor Pedrycz

path = input("Please, enter the path to the node list file")
fh=open("p2p-Gnutella08-mod.txt", "rb")
G=nx.read_adjlist(fh, create_using=nx.DiGraph(), nodetype=int)
fh.close()

gnodes = list(G.nodes())
def randomSurf(G,m,E):
    randsurf = {i:0 for i in gnodes}
    current = rn.choice(gnodes)
    randsurf[current] += 1
    for _ in range(E):
        tab = [x for x in G.neighbors(current)]
        if tab == [] or rn.random() <= m:
            current = rn.choice(gnodes)
            randsurf[current] += 1
        else:
            current = rn.choice(tab)
            randsurf[current] += 1
    for x,y in randsurf.items():
        randsurf[x] = y/E

    return sorted(randsurf, key=randsurf.get, reverse=True)[:10],sorted(randsurf.values(), reverse=True)[:10]

def pagerank(G,m,E):
    n = len(G.nodes)
    adj = np.zeros((n, n))
    for edge in G.edges:
        adj[int(edge[1]), int(edge[0])] = 1
    A = np.matrix(adj)
    D = np.matrix(np.zeros((n, n)))
    columnsum = adj.sum(axis=0)
    for i in range(n):
        if columnsum[i] == 0:
            D[:, i] = 1 / n
        else:
            for i1 in range(n):
                A[i1, i] = A[i1, i] / columnsum[i]
    S = A.copy()
    S[:, :] = 1 / n
    pageranking = {}
    rating = np.ones((n, 1)) / n
    #Reducing the amount of redundant calculations
    Dxk = D[0,:] * rating
    mSxk = m * sum(rating) / n
    for i in range(E - 1):
        rating = (1 - m) * (A * rating) + (1 - m) * Dxk + mSxk
    for i in range(n):
        pageranking[i] = rating[i, 0]
    return sorted(pageranking, key=pageranking.get, reverse=True)[:10],sorted(pageranking.values(), reverse=True)[:10]


print("Randomsurfer:")
print(randomSurf(G,0.15,10000000))
print("Pagerank:")
print(pagerank(G,0.15,10))
print("Iterations to stabilize the top 10:")
i = 0
x = []
while True:
    i+=1
    if i == 1:
        a,b = pagerank(G,0.15,i)
    if x == a:
        print(f"Around {i}")
        break
    x = a