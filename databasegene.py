from database import *
import ast
import re
from dft_utils import psd

import itertools


for n in range(3,40,2):
    print(f"Processing n = {n}")
    all_charm_bracelets = set()
    ones = (n+1) // 2 # 计算1的个数，假设n为奇数
    zeros = n - ones # 计算0的个数，假设n为奇数
        # 生成所有1的位置组合
    for ones_indices in itertools.combinations(range(n), ones):
        seq = [0] * n
        for idx in ones_indices:
            seq[idx] = 1
        cb = CharmBracelet(seq)
        all_charm_bracelets.add(cb)
    sorted_charm_bracelets = sorted(all_charm_bracelets, key=lambda cb: abs(cb.offset_1))
    with open(f"data/DecimationClass_{n}.txt", "w") as f:
        f.write(f"序列长度: {n} ")
        f.write(f"等价类总数: {len(all_charm_bracelets)} \n")
        f.write("等价类代表, 偏移量, 自适应兼容性, 能量\n")
        for cb in sorted_charm_bracelets:
            f.write(f"{cb.decimated_seq}, {cb.offset_1}, {cb.selfcompatible}, {cb.energy}\n")
    print(f"等价类总数: {len(all_charm_bracelets)}")
    count = 0
    pass_charm_bracelets = set()
    for cb in sorted_charm_bracelets:
        if abs(cb.offset_psd) < (n+1) / 4:
            pass_charm_bracelets.add(cb)
            count += 1
    print(f"满足条件的等价类代表总数: {count}")

    with open(f"data/DecimationClass_{n}_pass.txt", "w") as f:
        f.write(f"序列长度: {n}\n")
        f.write(f"满足条件的等价类代表总数: {count}\n")
        f.write("等价类代表, 偏移量, 自适应兼容性, 能量\n")
        for cb in pass_charm_bracelets:
            f.write(f"{cb.decimated_seq}, {cb.offset_1}, {cb.selfcompatible}, {cb.energy}\n")

    condidate_pairs = condidate_pair(pass_charm_bracelets)
    print(f"满足条件的等价类代表对数: {len(condidate_pairs)}")
    count = 0
    with open(f"data/LegendrePairs_{n}.txt", "w") as f:
        f.write(f"序列长度: {n}\n")
        f.write("等价类代表1, 能量, 等价类代表2, 能量\n")
        for cb1, cb2 in condidate_pairs:
            if checkcompatible(cb1, cb2):
                count += 1
                f.write(f"{cb1.decimated_seq} {cb1.energy} {cb2.decimated_seq} {cb2.energy}\n")
        print(f"Legendre对数: {count}")