'''
https://play.picoctf.org/practice/challenge/104
I wonder what this really is... enc ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

Solution
From the challenge in information.txt, i will do the following to better understand the binary file

Running binwalk -B did not reveal anything.
Hex editing did not reveal anything as well.

Google searching on how to view binary files, i came across the command cat

Running

cat enc

Gave a bunch of random Chinese characters. This can only help in that i know the encoding is not in ASCII.
It is NOT in ASCII
Also that the characters are all unique, so there is no pattern in the characters.
It could be either a hash or just an encoded text.
Since the hint mentions decoding, i assume that the text is encoded and we need to decode.

Here then, i should be looking for particular encoding to find the correct one to decode the text with.

The question also gave code:

''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

This one-liner should be broken down into smaller parts, as it is hard to read from this.

1. 
[chr((ord(flag[i]) << 8) + ord(flag[i + 1]))
2.
for i in range(0, len(flag), 2)])

For 1.
ord(flag[i]) => what is flag? probably the answer we want. The solution.
Position i. Here we see 2.
2. Suggests that the length of the string => jump in two characters.

Back to 1. So if the answer is 11 characters, "i" will be 0,2,4,6,8,10
Then for each of this "i", we access flag[i] and flag[i+1].

Here, we can tell that it will iterate through all the characters.
It iterates in pairs of characters.
ord(flag[i+1]) will touch indices 1,3,5,7,9 and 11. It returns the Unicode code point
of the encoded character in position i+1 in the flag string.


ord(flag[i]) << 8 will shift the Unicode code point 8 bits to the left.

So the algorithm will add the two code points together.

Then chr() converts the final result to a new character.

The ''.join is acting like a concatenation function, joining these new characters together.

So a rough outline of how to reverse this:
(X << 8) + Y = Z.
Z is what we see. An encoded character
We know Z. We need to figure out X and Y.
So X << 8 = Z - Y
and X = ( Z - Y ) >> 8

So the algorithm should be like:
X = (ord(Z) - Y) >> 8
Y = ord(Z) - ( X << 8 )
And the iterations + .join means we get of the form:
X_1 Y_1 X_2 Y_2 ... X_N Y_N

So there are two unknowns, X and Y, but we know there exists at least one permutation that yields Z_i
Two unknowns, three variables => Infinite solutions.
So we must look deeper for more clues.

Here, there is no additional clue. However, i noticed the 8 bits.
8 bits is a byte. So it is possible that X is shifted 8 bits to the left, then when you add Y, you get this new character
But then here we know that the actual flag is definitely of the form picoCTF{...}

High chance that the original picoCTF flag is in ASCII. If so, then each of the characters has 8 bits.
Then this also means that the 8 bits shift will then result in 16 bits.

So the final characters are of 16 bits, the first 8 bits will be the shifted 8, the second 8 bits is the Y_i
So X_iY_i = Z_i, 16 bits on LHS and RHS. X_i = Z_i >> 8 (Removes 8 bits on right). Y_i = Z_i && 0000 0000 1111 1111.
We can make use of bitwise AND to filter out the desired bits (8 bits on the right.)
'''

def extractRight8Bits(Zi):
    ANDmask = 0b0000000011111111
    return Zi & ANDmask

def extractLeft8Bits(Zi):
    return Zi >> 8

def decode(encodedTextString):
    decodedString = ''
    for character in encodedTextString:
        unicodeCodepoint = ord(character)
        decodedString += chr(extractLeft8Bits(unicodeCodepoint)) + chr(extractRight8Bits(unicodeCodepoint))
    print(decodedString)
    return decodedString

# The following Chinese characters in the input is the flag challenge in picoCTF: encoded text to decode
decode('灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸彤㔲挶戹㍽')