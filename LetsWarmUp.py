'''
https://play.picoctf.org/practice/challenge/22
If I told you a word started with 0x70 in hexadecimal, what would it start with in ASCII?

Solution:

A word is a byte. So 8 bits. 0x70 in hexadecimal can be denoted as two four-bit sections: 0 and 7

So 7 in 4-bits is 0111 and 0 is 4 bits is 0000. Concatenating them gives 0111 0000
We can use a python in built function.
'''

print(chr(0b1110000))

'''
Converter without in-built function
'''

def convertHexadecimalToBinary(binaryString):
    length = len(binaryString)-1
    decimalValue = 0
    for character in binaryString:
        decimalValue += int(character) * 2 ** length
        length -= 1
    return chr(decimalValue)

print(convertHexadecimalToBinary("1110000"))