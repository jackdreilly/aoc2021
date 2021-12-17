s = "target area: x=60..94, y=-171..-136"
x1, x2, y1, y2 = (
    c
    for b in s.split(": ")[1].strip().split(", ")
    for c in map(int, b.split("=")[1].split(".."))
)


def sim(px, py, vx, vy, maxy=0):
    return (
        maxy
        if (x1 <= px <= x2 and y1 <= py <= y2)
        else 0
        if ((not vx and not (x1 <= px <= x2)) or (px > x2) or (py < y1 and vy < 0))
        else sim(
            px + vx,
            py + vy,
            vx + (vx < 0 and 1 or vx > 0 and -1 or 0),
            vy - 1,
            max(maxy, py + vy),
        )
    )


print(max(sim(0, 0, i, j) for j in range(-abs(y1), abs(y1)) for i in range(x2 + 1)))
