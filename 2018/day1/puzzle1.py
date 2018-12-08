
frequency = 0

with open('input.txt', 'r') as fp:
    for line in fp:
        frequency = frequency + int(line)

print(frequency)
