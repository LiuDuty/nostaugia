import json
import math
import random
from pathlib import Path


ROWS = 5
COLS = 8
BOARD_W = 800
BOARD_H = 500
CELL_W = BOARD_W / COLS
CELL_H = BOARD_H / ROWS
TAB = 22
SEED = 4040


def cubic(points, x1, y1, x2, y2, x, y):
    points.append(["C", round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2), round(x, 2), round(y, 2)])


def line(points, x, y):
    points.append(["L", round(x, 2), round(y, 2)])


def edge(points, x1, y1, x2, y2, sign, horizontal):
    if sign == 0:
        line(points, x2, y2)
        return

    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    ux = dx / length
    uy = dy / length
    nx = -uy
    ny = ux

    depth = TAB * sign
    if not horizontal:
        depth = -TAB * sign

    a = 0.32
    b = 0.43
    c = 0.57
    e = 0.68
    p_a = (x1 + dx * a, y1 + dy * a)
    p_b = (x1 + dx * b, y1 + dy * b)
    p_c = (x1 + dx * c, y1 + dy * c)
    p_e = (x1 + dx * e, y1 + dy * e)
    mid = (x1 + dx * 0.5 + nx * depth, y1 + dy * 0.5 + ny * depth)

    line(points, *p_a)
    cubic(points, p_a[0] + ux * 8, p_a[1] + uy * 8, p_b[0] - nx * depth * 0.35, p_b[1] - ny * depth * 0.35, p_b[0], p_b[1])
    cubic(points, p_b[0] + nx * depth * 0.35, p_b[1] + ny * depth * 0.35, mid[0] - ux * 18, mid[1] - uy * 18, mid[0], mid[1])
    cubic(points, mid[0] + ux * 18, mid[1] + uy * 18, p_c[0] + nx * depth * 0.35, p_c[1] + ny * depth * 0.35, p_c[0], p_c[1])
    cubic(points, p_c[0] - nx * depth * 0.35, p_c[1] - ny * depth * 0.35, p_e[0] - ux * 8, p_e[1] - uy * 8, p_e[0], p_e[1])
    line(points, x2, y2)


def to_path(commands, ox=0, oy=0):
    out = []
    for cmd in commands:
        if cmd[0] == "M":
            out.append(f"M {cmd[1]-ox:.2f} {cmd[2]-oy:.2f}")
        elif cmd[0] == "L":
            out.append(f"L {cmd[1]-ox:.2f} {cmd[2]-oy:.2f}")
        elif cmd[0] == "C":
            out.append(
                f"C {cmd[1]-ox:.2f} {cmd[2]-oy:.2f} {cmd[3]-ox:.2f} {cmd[4]-oy:.2f} {cmd[5]-ox:.2f} {cmd[6]-oy:.2f}"
            )
        elif cmd[0] == "Z":
            out.append("Z")
    return " ".join(out)


def bounds(commands):
    xs = []
    ys = []
    for cmd in commands:
        nums = cmd[1:]
        xs.extend(nums[0::2])
        ys.extend(nums[1::2])
    return min(xs), min(ys), max(xs), max(ys)


def main():
    random.seed(SEED)
    vertical = [[random.choice([-1, 1]) for _ in range(COLS - 1)] for _ in range(ROWS)]
    horizontal = [[random.choice([-1, 1]) for _ in range(COLS)] for _ in range(ROWS - 1)]
    pieces = []

    for r in range(ROWS):
        for c in range(COLS):
            x0 = c * CELL_W
            y0 = r * CELL_H
            x1 = x0 + CELL_W
            y1 = y0 + CELL_H

            top = 0 if r == 0 else -horizontal[r - 1][c]
            right = 0 if c == COLS - 1 else vertical[r][c]
            bottom = 0 if r == ROWS - 1 else horizontal[r][c]
            left = 0 if c == 0 else -vertical[r][c - 1]

            cmds = [["M", round(x0, 2), round(y0, 2)]]
            edge(cmds, x0, y0, x1, y0, top, True)
            edge(cmds, x1, y0, x1, y1, right, False)
            edge(cmds, x1, y1, x0, y1, bottom, True)
            edge(cmds, x0, y1, x0, y0, left, False)
            cmds.append(["Z"])

            bx0, by0, bx1, by1 = bounds(cmds[:-1])
            margin = 2
            bx0 -= margin
            by0 -= margin
            bx1 += margin
            by1 += margin

            pieces.append({
                "id": r * COLS + c + 1,
                "row": r,
                "col": c,
                "path": to_path(cmds, bx0, by0),
                "coverPath": to_path(cmds, 0, 0),
                "targetX": round(bx0, 2),
                "targetY": round(by0, 2),
                "cellX": round(x0, 2),
                "cellY": round(y0, 2),
                "viewBox": [round(bx0, 2), round(by0, 2), round(bx1 - bx0, 2), round(by1 - by0, 2)],
                "localViewBox": [0, 0, round(bx1 - bx0, 2), round(by1 - by0, 2)],
                "imageX": round(-bx0, 2),
                "imageY": round(-by0, 2),
                "width": round(bx1 - bx0, 2),
                "height": round(by1 - by0, 2),
                "rotation": 0
            })

    payload = {"rows": ROWS, "cols": COLS, "boardWidth": BOARD_W, "boardHeight": BOARD_H, "pieces": pieces}
    out = Path(__file__).parent / "public" / "puzzle-pieces-40.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"generated {len(pieces)} pieces -> {out}")


if __name__ == "__main__":
    main()
