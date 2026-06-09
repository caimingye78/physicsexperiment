#!/usr/bin/env python3
"""
摆动波 (Pendulum Wave) 摆长计算脚本
=====================================

原理:
    单摆周期  T = 2*pi*sqrt(L/g)
    反解摆长  L = g * (T / (2*pi))**2

设计思路:
    选定一个"总循环时间" T_cycle (例如 60 秒)。
    让第 1 个(最长)摆在 T_cycle 内完成 base_osc 次全振动,
    第 k 个摆完成 (base_osc + k - 1) 次, 这样每个摆每分钟比前一个多摆 1 次,
    相位逐渐错开 -> 形成行波, 并在 T_cycle 后重新同步。

用法:
    python3 pendulum_lengths.py                 # 默认 15 个摆, 60 秒循环, 51 次起
    python3 pendulum_lengths.py -n 20 -c 60 -b 40 --csv lengths.csv
"""
import argparse
import csv
import math


def compute_lengths(n=15, t_cycle=60.0, base_osc=51, g=9.8, ball_radius_mm=0.0):
    """返回每个摆的参数列表。

    ball_radius_mm: 小球半径(毫米)。摆长指悬挂点到小球质心的距离,
    所以"线长" = 摆长 - 小球半径。
    """
    rows = []
    for k in range(1, n + 1):
        osc = base_osc + (k - 1)          # 该摆在 t_cycle 内的振动次数
        period = t_cycle / osc            # 单摆周期 T_k (s)
        length = g * (period / (2 * math.pi)) ** 2   # 摆长 L_k (m)
        string = length - ball_radius_mm / 1000.0    # 实际剪线长度 (m)
        rows.append({
            "index": k,
            "oscillations_per_cycle": osc,
            "period_s": period,
            "length_m": length,
            "length_cm": length * 100.0,
            "string_length_cm": string * 100.0,
        })
    return rows


def print_table(rows, t_cycle):
    print(f"\n总循环时间 T_cycle = {t_cycle:g} s   |   摆的数量 = {len(rows)}\n")
    header = f"{'#':>2}  {'每周期振动次数':>12}  {'周期 T (s)':>10}  {'摆长 (cm)':>10}  {'剪线长 (cm)':>11}"
    print(header)
    print("-" * len(header.encode("gbk", errors="replace")))
    for r in rows:
        print(f"{r['index']:>2}  {r['oscillations_per_cycle']:>12}  "
              f"{r['period_s']:>10.4f}  {r['length_cm']:>10.2f}  {r['string_length_cm']:>11.2f}")
    longest = rows[0]["length_cm"]
    shortest = rows[-1]["length_cm"]
    print(f"\n摆长范围: {shortest:.1f} cm  ~  {longest:.1f} cm  "
          f"(总跨度 {longest - shortest:.1f} cm)")
    print("提示: 释放角度建议小于 15 度, 公式才足够准确。\n")


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"已写入 CSV: {path}")


def write_json(rows, path, meta):
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "pendulums": rows}, f, ensure_ascii=False, indent=2)
    print(f"已写入 JSON: {path}")


def main():
    p = argparse.ArgumentParser(description="计算摆动波每个摆的长度")
    p.add_argument("-n", "--num", type=int, default=15, help="摆的数量 (默认 15)")
    p.add_argument("-c", "--cycle", type=float, default=60.0, help="总循环时间秒 (默认 60)")
    p.add_argument("-b", "--base", type=int, default=51, help="最长摆每周期振动次数 (默认 51)")
    p.add_argument("-g", "--gravity", type=float, default=9.8, help="重力加速度 (默认 9.8)")
    p.add_argument("-r", "--radius", type=float, default=0.0, help="小球半径 mm (默认 0)")
    p.add_argument("--csv", type=str, default=None, help="导出 CSV 文件路径")
    p.add_argument("--json", type=str, default=None, help="导出 JSON 文件路径")
    args = p.parse_args()

    rows = compute_lengths(args.num, args.cycle, args.base, args.gravity, args.radius)
    print_table(rows, args.cycle)

    meta = {
        "num": args.num, "t_cycle_s": args.cycle, "base_oscillations": args.base,
        "gravity": args.gravity, "ball_radius_mm": args.radius,
    }
    if args.csv:
        write_csv(rows, args.csv)
    if args.json:
        write_json(rows, args.json, meta)


if __name__ == "__main__":
    main()
