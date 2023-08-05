def topK(str, K):
    d = {}
    for c in str:
        d[c] = d.get(c, 0) + 1
    L = [(v, u) for u, v in d.items()]
    L.sorted(reversed=True)
    K = min(K, len(L))
    for i in range(K):
        print(L[i][1], L[i][0])