def topK(str, K):
    d = {}
    for c in str:
        d[c] = d.get(c, 0) + 1
    L = [(v, u) for u, v in d.items()]
    L.sort(reverse=True)
    K = min(K, len(L))
    for i in range(K):
        print(L[i][1], L[i][0])

if __name__ == '__main__':
    topK('Bach khoa Ha Noi', 2)