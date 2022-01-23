from random import randint


inputs = [
    [-1, -1],
    [13, 6],
    [15, 7],
    [15, 10],
    [11, 2],
    [-7, 15],
    [10, 8],
    [10, 1],
    [-5, 10],
    [15, 5],
    [-3, 3],
    [0, 5],
    [-5, 11],
    [-9, 12],
    [0, 10],
]
alpha, beta = zip(*inputs)
for i in range(1111111, 9999999):
    w1, w2, w3, w4, w6, w7, w9 = map(int, str(i))
    vars = w1, w2, w3, w4, w6, w7, w9
    if not all(vars):
        continue
    w5 = w4 + beta[4] + alpha[5]
    w8 = w7 + beta[7] + alpha[8]
    w10 = w9 + beta[9] + alpha[10]
    w11 = w6 + beta[6] + alpha[11]
    w12 = w3 + beta[3] + alpha[12]
    w13 = w2 + beta[2] + alpha[13]
    w14 = w1 + beta[1] + alpha[14]
    if all(1 <= w <= 9 for w in (w5, w8, w10, w11, w12, w13, w14)):
        print(i)
        print(
            "".join(
                map(str, (w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14))
            )
        )
        exit()
