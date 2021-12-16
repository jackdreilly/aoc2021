from pathlib import Path

s = "".join(
    bin(int(x, 16))[2:].rjust(4, "0") for x in Path("16.txt").read_text().strip()
)


def solve(s):
    if not s or not int(s, 2):
        return 0
    v, t, r = int(s[:3], 2), int(s[3:6], 2), s[6:]
    if t == 4:
        value = 0
        while True:
            kill = not r or r[0] == "0"
            value += int(r[:5], 2)
            r = r[5:]
            if kill:
                return v + solve(r)
    i, r = r[0], r[1:]
    if i == "0":
        tb, r = int(r[:15], 2), r[15:]
        return v + solve(r[:tb]) + solve(r[tb:])
    ns, r = int(r[:11], 2), r[11:]
    return v + solve(r)


print(solve(s))
