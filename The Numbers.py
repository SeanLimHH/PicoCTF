'''
https://play.picoctf.org/practice/challenge/68?page=3

Description:

The numbers... what do they mean?

Solution:

The attached flag is "the_numbers.png".
In the image are these numbers and characters:

16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }

On first glance, i can guess it is in some encoding.

To be fair, the flag is always in picoCTF{} .. so in the image there is this pattern.

It is also possible it is some caesar-cipher pattern; where the letters are just rotated.

One trick i learnt from one of the challenges: if the characters have a pattern: it is likely to
be encoding or decoding. If no pattern, likely to be either encoding or decoding or hashed value.
Means some encryption.

We can use this to figure out: here the only structure we see is that the numbers never exceed 21.
This reminds me of a caesar cipher challenge. Because the English alphabet only has 26 letters,
this is possible.

ABCD EFGH IJKL MNOP QRST UVWX YZ

This is similar to ROT13.
So we can see P matches MNOP, which is index 16.
I is index 9 as well.
So the author is just using this English Alphabet as a keyset for Caesar Cipher encryption.

This might be slightly because i have done a few challenges that i can figure this out.
I am unsure if the author intended for this, i know the CTF flag structure hence this pattern struck out to me.

Anyways, we can write a Python function to decrypt this.

The answer is picoctfthenumbersmason without the curly braces.

Just adding it back to the position we get then:
picoctf{thenumbersmason}
'''

KEYSET = "abcdefghijklmnopqrstuvwxyz"
encryptedText = [16,9,3,15,3,20,6,20,8,5,14,21,13,2,5,18,19,13,1,19,15,14]

def caesarCipherDecrypt(keyset, encryptedText):
    flagText = ''
    for character in encryptedText:
        flagText += keyset[character-1]
    print("Flag without curly braces:", flagText)
    return flagText

caesarCipherDecrypt(KEYSET, encryptedText)