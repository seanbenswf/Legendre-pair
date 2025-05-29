from necklaces_generation import find_charm_bracelet
from integer_utils import relative_primes
from dft_utils import psd
import numpy as np
import itertools

class CharmBracelet:
    def __init__(self, seq):

        self.seq = tuple(find_charm_bracelet(seq))
        l = len(seq)
        offset = (l + 1) / 4
        psd_vals = psd(seq)
        offset_psds = [v - offset for v in psd_vals[1:]]
        max_offset_val = 0
        max_decimated = None
        max_decimation_idx = None
        max_psd = max(offset_psds, key=abs)

        # 找到使abs(offset_psds[d-1])最大的d
        d_star = max(relative_primes(l), key=lambda d: abs(offset_psds[d-1]))
        max_offset_val = offset_psds[d_star-1]
        max_decimation_idx = pow(d_star, -1, l)
        max_decimated = [seq[(k * max_decimation_idx) % l] for k in range(l)]
        # for d in relative_primes(l):
        #     # 找u1最大偏移
        #     # abs_offset = max(offset_psds, key=abs)
        #     abs_offset = offset_psds[d-1]
        #     if abs(abs_offset) > abs(max_offset_val):
        #         max_offset_val = abs_offset
        #         max_decimation_idx = pow(d, -1, l)

        # 判断是否存在相反数
        found_opposite = False
        for d2 in relative_primes(l):
            if d2 == d_star:
                continue
            if abs(offset_psds[d2-1] + max_offset_val) < 1e-6:
                found_opposite = True
                break

        self.psd = offset_psds
        self.offset_psd = max_psd
        self.offset_1 = max_offset_val
        self.decimation_idx = max_decimation_idx
        self.decimated_seq = max_decimated
        self.selfcompatible = found_opposite
        self.energy = sum(i**2 for i in compute_paf(seq))  # PAF能量

    def __eq__(self, other):
        return self.seq == other.seq

    def __hash__(self):
        return hash(self.seq)

    def __repr__(self):
        return (f"CharmBracelet(seq={self.seq}, offset_1={self.offset_1}, "
                f"compatible={self.selfcompatible})")

def compute_paf(seq):
    """
    计算序列的部分自相关函数（PAF），忽略 shift=0。
    返回长度为 (N-1)//2 的数组。
    """
    N = len(seq)
    shifts = np.arange(1, (N - 1) // 2 + 1)
    # 构造所有需要的移位矩阵
    rolled = np.array([np.roll(seq, k) for k in shifts])
    # 广播乘法并按行求和
    paf = np.dot(rolled, seq)
    return paf

def check_legendre_pair(a, b, c):
    """验证 a, b 是否为 Legendre pair"""
    paf_a = compute_paf(a)
    paf_b = compute_paf(b)
    sum_paf = paf_a + paf_b
    # print(f"PAF a: {paf_a}, PAF b: {paf_b}, Sum PAF: {sum_paf}")
    diffs = sum_paf - c
    max_err = np.max(np.abs(diffs))
    return max_err == 0

def checkcompatible(x,y):
    """
    检查两个charm bracelet是否兼容
    """
    flag = False
    c = (len(x.seq) + 1) // 2
    for d in relative_primes(len(x.seq)):
        if abs(x.psd[d-1] + y.offset_1) < 1e-6:
            D = pow(d, -1, len(x.seq))
            decimated_x = [x.seq[(k * D) % len(x.seq)] for k in range(len(x.seq))]
            flag = check_legendre_pair(decimated_x, y.decimated_seq, c)
            if flag:
                break
    return flag


def condidate_pair(all_charm_bracelets):
    pairs = []
    used = set()
    for cb in all_charm_bracelets:
        if cb.selfcompatible:
            pairs.append((cb, cb))
    # 遍历所有charm bracelet的组合
    for cb1, cb2 in itertools.combinations(all_charm_bracelets, 2):
        if abs(cb1.offset_1 + cb2.offset_1) < 1e-8:
            # 避免重复分组
            if (cb1, cb2) not in used and (cb2, cb1) not in used:
                pairs.append((cb1, cb2))
                used.add((cb1, cb2))
                used.add((cb2, cb1))
    return pairs



# all_charm_bracelets = set()
# n = 9
# ones = (n+1) // 2 # 计算1的个数，假设n为奇数
# zeros = n - ones # 计算0的个数，假设n为奇数

# 生成所有1的位置组合
# for ones_indices in itertools.combinations(range(n), ones):
#     seq = [0] * n
#     for idx in ones_indices:
#         seq[idx] = 1
#     cb = CharmBracelet(seq)
#     all_charm_bracelets.add(cb)
# sorted_charm_bracelets = sorted(all_charm_bracelets, key=lambda cb: abs(cb.offset_1))
# print(f"等价类总数: {len(all_charm_bracelets)}")
# print("等价类代表:")
# count = 0
# for cb in sorted_charm_bracelets:
#     if abs(cb.offset_psd) < (n+1) / 4:
#         print(cb)
#         count += 1
# print(f"满足条件的等价类代表总数: {count}")

# 生成所有长度为n的charm bracelet等价类

