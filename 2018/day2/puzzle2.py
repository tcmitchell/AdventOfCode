
import collections

def count_diffs(seq1, seq2):
    return sum(1 for a, b in zip(seq1, seq2) if a != b)

def load_box_ids(fname):
    with open(fname, 'r') as fp:
        return [line.strip() for line in fp]

def find_the_pair(box_ids):
    num_box_ids = len(box_ids)
    for i in range(num_box_ids):
        seq1 = box_ids[i]
        for j in range(i, num_box_ids):
            seq2 = box_ids[j]
            if count_diffs(seq1, seq2) == 1:
                return seq1, seq2

box_ids = load_box_ids('input.txt')
id1, id2 = find_the_pair(box_ids)
print('The pair of ids is {} and {}'.format(id1, id2))
common_id = ''.join([a for a, b in zip(id1, id2) if a == b])
print('The common characters are {}'.format(common_id))
