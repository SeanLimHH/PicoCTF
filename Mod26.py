'''
https://play.picoctf.org/practice/challenge/144

Description:
Cryptography can be easy, do you know what ROT13 is?

Solution:
Caesar's cipher just involves translating (shifting) characters down a fixed keyset. Alphabetical traditionally.
ROT13 uses the following lookup table, so there are 26 characters only
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
Also, doing ROT13 twice will yield the original; ROT13 is a reciprocal cipher
'''

alphabetKeyset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
wordToShift = input("To shift by 13 characters:")
newWord = ''
for character in wordToShift:
    found = alphabetKeyset.find(character)
    if found != -1:
        newWord += alphabetKeyset[(found+13)%26]
    else:
        newWord += character
print(newWord)
