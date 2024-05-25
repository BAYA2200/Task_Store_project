def count(n):
    for i in range(1, n + 1):
        a = str(i) * i
        print(' '.join(a))


count(10)