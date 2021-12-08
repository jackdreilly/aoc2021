from pathlib import Path

print(
    sum(
        1
        for line in Path("i8.txt").read_text().split("\n")
        if line
        for x in line.split(" | ")[1].split(" ")
        if len(x) in {2, 3, 4, 7}
    )
)
