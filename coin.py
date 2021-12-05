import random
from scipy.special import beta, binom

rounds = 100000
n = 9


x = []
for _ in range(rounds):
    p = random.random()
    x.append(sum(random.random() < p for _ in range(n)) == n / 2)
print(sum(x) / rounds)

print(beta(n/2 + 1, n/2 + 1) * binom(n, n/2))
