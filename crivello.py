# Funzione che restituisce una lista di numeri primi fino a n
def crivello(n):
    l = list(range(2, n + 1))
    for i in range(2, int(n**0.5) + 1):
        if i in l:
            for j in range(i * 2, n + 1, i):
                if j in l:
                    l.remove(j)
    return l

print(crivello(100))

