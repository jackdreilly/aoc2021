from pathlib import Path

lines = [x.split(' ') for x in Path("d1b.txt").read_text().splitlines()]
h,v = 0,0
for a,b in lines:
    b = int(b)
    if a == 'forward':
        h += b
    if a == 'down':
        v -= b
    if a == 'up':
        v += b
print(abs(h * v))
