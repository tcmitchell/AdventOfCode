
import collections

cksum2 = 0
cksum3 = 0

with open('input.txt', 'r') as fp:
    for line in fp:
        letter_counts = collections.Counter(line.strip()).values()
        if 2 in letter_counts:
            cksum2 += 1
        if 3 in letter_counts:
            cksum3 += 1

cksum = cksum2 * cksum3
print('The checksum is {}'.format(cksum))
