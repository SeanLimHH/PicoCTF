'''
https://play.picoctf.org/practice/challenge/58?page=3

Description:
What is 0x3D (base 16) in decimal (base 10)?

Solution:
The following function is written to convert.
'''

def solutionOne(inputHexadecimal): # In-built function.

    # or even without casting this will work:
    # return inputHexadecimal
    return int(inputHexadecimal)
print("Solution one:", solutionOne(0x3D))

def solutionTwo(inputHexadecimal): # No in-built function; input as string
    hexadecimalDigits = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    inputHexadecimal = inputHexadecimal[2:]

    position = len(inputHexadecimal) - 1
    total = 0
    for character in inputHexadecimal:
        total += hexadecimalDigits.index(character) * 16 ** position
        position -= 1
    return total

print("Solution two:", solutionTwo('0x3D'))