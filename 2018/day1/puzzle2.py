

import itertools

frequency = 0
seen_freqs = dict()
seen_freqs[frequency] = None

with open('input.txt', 'r') as fp:
    freqs = [int(line) for line in fp]

pool = itertools.cycle(freqs)

for item in pool:
    frequency = frequency + item
    if frequency in seen_freqs:
        break
    else:
        seen_freqs[frequency] = None

print(frequency)

