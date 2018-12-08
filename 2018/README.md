Extract all integers from a line of input:

```
claims = map(lambda s: map(int, re.findall(r'-?\d+', s)), data)
```
