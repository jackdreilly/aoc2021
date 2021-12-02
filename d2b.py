from pathlib import Path

lines = [x.split(' ') for x in Path("d2.txt").read_text().splitlines()]
h,v, vv = 0,0, 0
for a,b in lines:
    b = int(b)
    if a == 'forward':
        h += b
        vv += b * v
    if a == 'down':
        v -= b
    if a == 'up':
        v += b
print(abs(h * vv))
