'''
https://play.picoctf.org/practice/challenge/162

Description:
In RSA, a small e value can be problematic, but what about N? Can you decrypt this? values

Attached is a values.txt:
Decrypt my super sick RSA:
c: 861270243527190895777142537838333832920579264010533029282104230006461420086153423
n: 1311097532562595991877980619849724606784164430105441327897358800116889057763413423
e: 65537

Solution:

RSA encryption
From school:
RSA is asymmetric. So public key =/= private key
We learnt that RSA's big idea is this: You have a very very large number from p and q.
This number can be presented as n = pq. The sender decides p and q with the following properties:

p and q are two unknown very large prime numbers and are coprime.
This means there is no common factors between p and q except 1.
In other words, their greatest common divisor (GCD) is 1.

Then, we compute Euler's totient function value, t(pq) = (p-1)(q-1).
Euler's totient function counts the number of positive integers lesser than its input that is coprime to input.

We have p and q which are prime. This means t(p) = p-1. t(q) = q-1.
The 1 represents the integer 1 which is the only number that can be divided by p and q individually.
So t(pq) = t(p)t(q) = (p-1)(q-1)
For the above, the trickiest part is t(pq) = t(p)t(q).
Because there are p-1 numbers that are not divisors of p and q-1 numbers that are not divisors of q,
there will be (p-1) * (q-1) numbers that are not divisors of p * q.

Then, we compute the public key e which should be coprime to totient t(pq).
This public key is passed to the public; anyone who wants to message the person, along with pq.

So this e is used with another variable d such that d = (e^-1) % totient(pq).
d is a modular inverse. It serves as a key to decrypt the cipher text. e is for encrypting plain text.
This d is the private key; not to be shared.

To encrypt: people use the public keys e and pq to encrypt a message
message^e % pq

To decrypt: the owner of this RSA key-pair uses private key d to decrypt the encrypted message received.
message = cipher^d % pq

RSA is known to be strong because of the difficulty in finding p and q given pq.
Difficult to find factors of very very large numbers.

In this question, n = pq = 1311097532562595991877980619849724606784164430105441327897358800116889057763413423
e is also given. We are lacking d to decrypt.

If we can find p or q it will help us decrypt as well.

totient(n) = totient(pq) = (p-1)(q-1) = 1311097532562595991877980619849724606784164430105441327897358800116889057763413423

Above we have seen that d = (e^-1) % totient(pq).

The problem is we do not know what totient(pq) is.

totient(pq) = (p-1)(q-1) = p*q - p - q + 1 = n - p - q + 1.

totient(pq) = n + 1 - p - q

So we have to figure out p and q from the given n.
This is the focus we need.

Here, i need to write code or find something that can factor n very very efficiently.

Googling search for an efficient calculator, i found this website:
http://factordb.com

Which gave two numbers 1955175890537890492055221842734816092141 and 670577792467509699665091201633524389157003

so p = 1955175890537890492055221842734816092141 and q = 670577792467509699665091201633524389157003
Then, we know:
message = cipher^d % pq

We need to find d: (e^-1) % totient(pq). See the code below.

Then the plaintext in number is: 13016382529449106065927291425342535437996222135352905256639573959002849415739773

From here, the number was very large and i had difficulties converting to ascii which is the flag's format.
I had to search up for this part.

But then after Google searching, the trick was to convert to hexadecimal first.
Then it is a string. So then i extracted out the 0x prefix.

So the flag is: picoCTF{sma11_N_n0_g0od_13686679}

'''
n = 1311097532562595991877980619849724606784164430105441327897358800116889057763413423
cipher = 861270243527190895777142537838333832920579264010533029282104230006461420086153423
p = 1955175890537890492055221842734816092141 # from factordb.com
q = 670577792467509699665091201633524389157003 # from factordb.com
d = pow(65537, -1, (p-1)*(q-1))
plaintext = pow(cipher, d, n)
print("Plain text in number:", plaintext)
plaintextInHexadecimal = hex(plaintext)
print("Hex string of plain text:", plaintextInHexadecimal)
plaintextInHexadecimalWithoutPrefix = plaintextInHexadecimal[2:]
print("Hex string of plain text without prefix:", plaintextInHexadecimalWithoutPrefix)
byteArray = bytearray.fromhex(plaintextInHexadecimalWithoutPrefix)
print("Byte array of plain text:", byteArray)
plainTextInASCII = byteArray.decode("ASCII")
print("Plain text:", plainTextInASCII)