from cs50 import *

from cs50 import get_int

height = 0
while height > 8 or height < 1:
    height = get_int("Height: ")

# Loop through rows and then columns
for i in range(1, height + 1):
    for j in range(1, height + 1):
        # Start printing # after correct number of spaces
        if j > (height - i):
            print("#", end="")
        else:
            print(" ", end="")
        # Print middle space and remaining #
        if j == height:
            print(" ", "#" * i, end="")
    print()