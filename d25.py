from pathlib import Path


data = Path("d25.txt").read_text().strip().splitlines()
n_rows, n_cols = len(data), len(data[0])
h = {(r, col) for r, row in enumerate(data) for col, c in enumerate(row) if c == ">"}
v = {(r, col) for r, row in enumerate(data) for col, c in enumerate(row) if c == "v"}

round = 0
while True:
    # for row in range(n_rows):
    #     print(
    #         "".join(
    #             ">" if (row, col) in h else "v" if (row, col) in v else "."
    #             for col in range(n_cols)
    #         )
    #     )
    round += 1
    both = h | v
    prop_h = {(row, (col + 1) % n_cols) for row, col in h}
    move_h = prop_h - both
    remove_h = {(row, (col - 1) % n_cols) for row, col in move_h}
    h = (h - remove_h) | move_h
    both = h | v
    # for row in range(n_rows):
    #     print(
    #         "".join(
    #             ">" if (row, col) in h else "v" if (row, col) in v else "."
    #             for col in range(n_cols)
    #         )
    #     )

    prop_v = {((row + 1) % n_rows, col) for row, col in v}
    move_v = prop_v - both
    remove_v = {((row - 1) % n_rows, col) for row, col in move_v}
    v = (v - remove_v) | move_v
    if not move_h and not move_v:
        break

print(round)
