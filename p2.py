def ternary(n):
    if n == 0:
        return "0"
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return "".join(nums)


a = 1
t = []
n = 5000
for _ in range(n):
    a *= 2
    # print(ternary(a),a, sum(map(int, ternary(a))))
    t.append(sum(map(int, ternary(a))))
diffs = [int(b) - int(a) for a,b in zip(t, t[1:])]
i = 0
m = 0
for j, d in enumerate(diffs):
    if d < 0:
        m =  max(m, j - i)
        i = j
print(m)
