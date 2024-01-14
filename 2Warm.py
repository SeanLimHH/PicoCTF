'''
https://play.picoctf.org/practice/challenge/86?page=3

Description:

Can you convert the number 42 (base 10) to binary (base 2)?

Solution:

This is similar to Warmed Up.py, but now it is base 10 to binary.
My answer is modified from my answer in the Warmed Up.py.

How one solution works is this:

There is a formula for the binary system:
https://www.pw.live/exams/school/binary-formula/

The expression is of the form:

    D = (an-1 × 2^(n-1)) + … + (a₃ × 2^3) + (a₂ × 2^2) + (a₁ × 2^1) + (a₀ × 2^0).

This is to express a decimal number in a binary representation.

Using this, we can rephrase as a summation:

    D = summation_(i=0)^(i=n-1) { a_i x 2^i}


Solution two's idea:

For each division by two, we are essentially increasing from 2^0 to 2^1 to ... 2^n
Eventually, the remainder will reach 0 or 1.
So in each loop, we are increasing the powers. We are seeing how many 2^i can fit inside
the number.
The first loop already handles the remainder. If let us say the first loop has 65,

65 % 2 = 1, hence in position 2^0 you will see it is equal to this, equal to 1.

Then we take the floor, so we get 65 // 2 = 32.
Then here we are dealing with 2^1. 32 % 2 = 0, means in the 2^1 position, we have 0.

The sequence will be as follows:
65 // 2 = 32 R 1 ===== 1 * 2^0 = 1
32 // 2 = 16 R 0 ===== 0 * 2^1 = 0
16 // 2 = 8 R 0 ===== 0 * 2^2 = 0
8 // 2 = 4 R 0 ===== 0 * 2^3 = 0
4 // 2 = 2 R 0 ===== 0 * 2^4 = 0
2 // 2 = 1 R 0 ===== 0 * 2^5 = 0
1 // 2 = 0 R 1 ===== 1 * 2^6 = 64

65 = 1 * 2^0 + 0 * 2^1 + 0 * 2^2 + 0 * 2^3 +  0 * 2^4 + 0 * 2^5 + 1 * 2^6
Then reverse, from 2^6 to 2^0 position-wise, we get:
65 = 0b100001

Each iteration left-shifts essentially, increasing by powers of 2.

The flag is thus: picoCTF{101010}
'''

def solutionOne(inputDecimal): # In-built function.

    # or even without casting this will work:
    # return inputDecimal
    return bin(inputDecimal)

print("Solution one:", solutionOne(42))

def solutionTwo(inputDecimal): # No in-built function; input as decimal

    # Divide by two and add the remainder method
    binaryStringToReverse = ''
    while inputDecimal != 0:
        
        divisibleByTwo = inputDecimal % 2 
        binaryStringToReverse += str(divisibleByTwo)
        inputDecimal = inputDecimal // 2

    return "0b" + binaryStringToReverse[::-1]

print("Solution two:", solutionTwo(42))