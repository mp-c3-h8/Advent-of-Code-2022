import os.path
from collections import defaultdict


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

# just a counter for every digit
count = defaultdict(int)
for snafu in data.splitlines():
    for i, digit in enumerate(reversed(snafu)):
        match digit:
            case "-": n = -1
            case "=": n = -2
            case _: n = int(digit)
        count[i] += n

# we dont need decimal at all, but here it is
print("Decimal:", sum(5**i*c for i, c in count.items()))


# handling negative digits:
# example: -3 = 2 (mod 5):
# -3 * 5^n = -5^(n+1) + 2 * 5^n
#
# converting 4 = -1 (mod 5) to "-":
# 4 * 5^n = 5^(n+1) -1 * 5^n
#
# converting 3 = -2 (mod 5) to "="
# 3 * 5^n = 5^(n+1) -2 * 5^n
carry = 0
snafu = ""
for i, digit in count.items():
    rem = (digit+carry) % 5
    carry = (digit+carry) // 5
    # so far regular base 5 conversion
    # snafu extra step:
    carry += rem // 3  # add 1 if rem == 3 or rem == 4
    snafu = str(rem) + snafu

# number is wrong without replacement
snafu = snafu.replace("3", "=").replace("4", "-")

print("Part 1: ", snafu)
