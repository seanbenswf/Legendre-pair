from sequence_generation import seq_binary
from vector_utils import rotate_n, reverse, rotate_right
from integer_utils import relative_primes

# 计算序列的necklace（所有旋转中字典序最小的序列）
def find_necklace(sequence):
    potential_necklace = sequence.copy()
    for k in range(1, len(sequence)):
        rotated_sequence = rotate_n(sequence, k)
        if potential_necklace > rotated_sequence:
            potential_necklace = rotated_sequence
    return potential_necklace

# 判断两个序列是否属于同一个necklace类
def equal_necklaces(sequence_a, sequence_b):
    return find_necklace(sequence_a) == find_necklace(sequence_b)

# 生成下一个prenecklace（用于necklace枚举算法）
def next_prenecklace(sequence):
    len_sequence = len(sequence)
    largest_index_equal_to_zero = find_largest_index_equal_to_zero(sequence)

    if largest_index_equal_to_zero is None:
        return None

    mod_sequence = sequence[:largest_index_equal_to_zero] + [1]
    t = len_sequence // (largest_index_equal_to_zero + 1)
    j = len_sequence % (largest_index_equal_to_zero + 1)

    return repeat_tth_times_and_fill_jth_values(mod_sequence, t, j)

# FKM算法：枚举[start, end]区间内的necklace
def fkm_algorithm(start, end):
    if len(start) != len(end):
        return None

    l = len(start)
    start_necklace = find_necklace(start)
    end_necklace = find_necklace(end)

    current = min(start_necklace, end_necklace)
    real_end = max(start_necklace, end_necklace)

    yield current

    while current < real_end:
        i = find_largest_index_equal_to_zero(current) + 1
        t = l // i
        j = l % i

        mod_current = current[: i - 1] + [1]
        current = repeat_tth_times_and_fill_jth_values(mod_current, t, j)
        if j == 0:
            yield current

# 枚举所有长度为length、1的个数为length//2的necklace
def seq_necklaces_of_half_density(length):
    density = length // 2
    current = [0] * (length - density) + [1] * density
    last_necklace = [(i + 1) % 2 for i in range(length)]
    last_necklace[0] = 0

    yield current
    while current < last_necklace:
        i = find_largest_index_equal_to_zero(current) + 1
        t = length // i
        j = length % i

        mod_current = current[: i - 1] + [1]
        current = repeat_tth_times_and_fill_jth_values(mod_current, t, j)
        if j == 0 and sum(current) == density:
            yield current
    return

# 找到序列中最后一个0的下标
def find_largest_index_equal_to_zero(sequence):
    for k in range(len(sequence) - 1, -1, -1):
        if sequence[k] == 0:
            return k
    return None

# 将sequence重复t次并补上前j个元素
def repeat_tth_times_and_fill_jth_values(sequence, t, j):
    return sequence * t + sequence[:j]

# 计算bracelet（旋转和翻转后字典序最小的序列）
def find_bracelet(sequence):
    potential_bracelet = sequence.copy()
    for n in range(len(sequence)):
        rotated_sequence = rotate_n(sequence, n)
        if rotated_sequence > potential_bracelet:
            potential_bracelet = rotated_sequence
        reverse_rotated_sequence = reverse(rotated_sequence)
        if reverse_rotated_sequence > potential_bracelet:
            potential_bracelet = reverse_rotated_sequence
    return potential_bracelet

# 只对necklace做翻转旋转，找bracelet
def find_bracelet_from_necklace(sequence):
    potential_bracelet = sequence.copy()
    reverse_sequence = reverse(sequence)
    for n in range(len(sequence)):
        reverse_rotated_sequence = rotate_n(reverse_sequence, n)
        if reverse_rotated_sequence > potential_bracelet:
            potential_bracelet = reverse_rotated_sequence
    return potential_bracelet

# 枚举所有长度为length、1的个数为length//2的bracelet
def seq_bracelets_of_half_density(length):
    density = length // 2
    current = [0] * (length - density) + [1] * density
    last_necklace = [(i + 1) % 2 for i in range(length)]
    last_necklace[0] = 0

    yield current
    while current < last_necklace:
        i = find_largest_index_equal_to_zero(current) + 1
        t = length // i
        j = length % i

        mod_current = current[: i - 1] + [1]
        current = repeat_tth_times_and_fill_jth_values(mod_current, t, j)
        if (
            j == 0
            and sum(current) == density
            and current == find_bracelet_from_necklace(current)
        ):
            yield current
    return

# 对输入序列集合去除bracelet等价类重复
def seq_bracelets(sequences):
    observed_sequences = set()
    for seq in sequences:
        if tuple(seq) not in observed_sequences:
            seen_seq = seq.copy()
            for k in range(len(seen_seq)):
                seen_seq = rotate_right(seen_seq)
                observed_sequences.add(tuple(seen_seq))
                observed_sequences.add(tuple(reverse(seen_seq)))
            yield seq
    return

# 计算charm bracelet（旋转+decimation后字典序最小的序列）
def find_charm_bracelet(sequence):
    charm_bracelet = sequence.copy()
    l = len(sequence)
    for rotation in range(l):
        for decimation in relative_primes(l):
            possible_bracelet = [
                sequence[(i * decimation + rotation) % l] for i in range(l)
            ]
            if possible_bracelet > charm_bracelet:
                charm_bracelet = possible_bracelet
    return charm_bracelet

# 判断序列是否为charm bracelet的最小代表
def is_charm_bracelet(sequence):
    charm_bracelet = sequence.copy()
    l = len(sequence)
    for rotation in range(l):
        for decimation in relative_primes(l):
            possible_bracelet = [
                sequence[(i * decimation + rotation) % l] for i in range(l)
            ]
            if possible_bracelet < charm_bracelet:
                return False
    return True

# 过滤出所有charm bracelet代表
def filter_by_charm_bracelet(sequences):
    for sequence in sequences:
        if is_charm_bracelet(sequence):
            yield sequence

def main():  # pragma: no cover
    print("Entry point for playing around")

if __name__ == "__main__":  # pragma: no cover
    main()
