'''
https://play.picoctf.org/practice/challenge/125?page=2

Description:
A one-time pad is unbreakable, but can you manage to recover the flag? 
(Wrap with picoCTF{}) nc mercury.picoctf.net 36981 otp.py

The otp.py file:
#!/usr/bin/python3 -u
import os.path

KEY_FILE = "key"
KEY_LEN = 50000
FLAG_FILE = "flag"


def startup(key_location):
	flag = open(FLAG_FILE).read()
	kf = open(KEY_FILE, "rb").read()

	start = key_location
	stop = key_location + len(flag)

	key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), flag, key))
	print("This is the encrypted flag!\n{}\n".format("".join(result)))

	return key_location

def encrypt(key_location):
	ui = input("What data would you like to encrypt? ").rstrip()
	if len(ui) == 0 or len(ui) > KEY_LEN:
		return -1

	start = key_location
	stop = key_location + len(ui)

	kf = open(KEY_FILE, "rb").read()

	if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), ui, key))

	print("Here ya go!\n{}\n".format("".join(result)))

	return key_location


print("******************Welcome to our OTP implementation!******************")
c = startup(0)
while c >= 0:
	c = encrypt(c)


Solution:
The first step i did was to run the file - to figure out generally what this challenge
is about. It gave this error:


******************Welcome to our OTP implementation!******************
Traceback (most recent call last):
    c = startup(0)
        ^^^^^^^^^^
    flag = open(FLAG_FILE).read()
            ^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'flag'

From this, FLAG_FILE constant; we can infer that there should be a flag called "flag"
in the same directory.

Then i read the code. There is not much information for now.

Then i read the challenge description. There is a netcat command in it.

Running it in WSL: we get:

******************Welcome to our OTP implementation!******************
This is the encrypted flag!
5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c

What data would you like to encrypt?



Typing in a character or series of characters returns a new random string.
The program is encrypting what the user inputs.

When we also read the code, key_location is returned and is equal to
5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c.

This key_location meaning, based on the code:
it is an index. key_location is the starting index, key_location + len(flag) is ending index.
Of a string. Which is kf => which is KEY_FILE = "key".

Then, this startup() function returns > 0, so it invokes encrypt(c) where c is the
return value of this startup() function, which is key_location.

key_location is first equal to 0. It then is reassigned.
Then the program runs encrypt(key_location)

Analysing the startup function:

The result variable is computed like this:

p = flag, k = key. A lambda function will compute ord(p) ^ k.
Then you see there is two iterables: `flag` and `key`.
Within the function:

	flag = open(FLAG_FILE).read()

and

	kf = open(KEY_FILE, "rb").read()
	key = kf[start:stop]

flag will be opened with default set to "r", read-only.
.read() returns the whole bytes of the whole file, by default.

So `flag` = opens the FLAG_FILE and returns all its bytes.

kf is in binary mode, also read-only. But it will have all the bytes of KEY_FILE
the key reads specific indices of this kf file.

So `key` = opens the KEY_FILE and returns specific bytes based on index.

Then "{:02x}" is the formatting in Python for 2 digit hexadecimals, hexadecimal is from the 'x'.

This function is revealing one thing: the main operation being performed to create
the returned output is ord(p) ^ k.

The ^ operator is the bitwise exclusive OR (XOR). This is standard in the OTP. And we can confirm it is
following the standard OTP algorithm.

The rationale, from school, is that an ideal cipher has each bits in 50-50 or 50% chance
of being either 1 or 0. This ideal cipher is ideal in the sense that it maximises uncertainty of
whether each bit is 1 or 0.

Another way to understand this is to look at an XOR truth table. See the output part:
When the output bit is `1`, you cannot tell (you are at 50-50) whether the P bits are 1 or 0 and whether
the Q bits are 1 or 0.
Similar idea for when the output bit is `0`.

So ord(p) ^ k will iterate, for each bit in p, perform an XOR of the bit value.

If k = 1, and the output we know is 0, using a truth table, we can tell that the
p bit (the bit in the flag) is 1.

Similarly,
If k = 1 and the output we know is 1, using a truth table, we can tell that the
p bit (the bit in the flag) is 0

If k = 0 and the output we know is 1, using a truth table, we can tell that the
p bit (the bit in the flag) is 0.


... This pattern continues. Here we do know that we can figure out two variables here:
output bit and k bit. p bit is unknown. Hence the solution is within this part.

One property of the XOR function is doing it twice yields the original values.

So 0bZZZZ XOR 0b1100 XOR 0b1100 = 0bZZZZ

I think this concept is necessary to find the flag.

We can, then XOR the key with the output to get the flag.

So the problem reduces to just find the bits of the key.

I then see the code: then I realise how they implemented this key.
In fact, if you let len(ui) = 0, you would, theoretically, be able to figure out
key_location, which is the starting index of our desired key.

But there is an if condition that will prevent undesirable user inputs like this.

So looking further for the implementation, we see:

	if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]
	key_location = stop

This part is actually useful.
One can deduce that the output wraps over if the stop >= KEY_LEN.

	stop = key_location + len(ui)

So if we spam the user input with many characters, the output will wrap over.

Reading the code again, the 

	if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]
	key_location = stop

part definitely has the answer to what is going on.

So if we try `a`, then `aa`, then `aaa`, all the way until it starts to repeat.

Going back, we can see that the encrypted flag has 64 characters:
len("5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c")

Also note that the output is formatted in hexadecimal, it means that there are half the number of bytes.
Which is 32 bytes; 32 readable characters.

Here, we see that on first run,

in encrypt(key_location), the key_location is equal to:
    
	stop = key_location + len(flag)

in startup().
Meaning to say. On first run, the key_location start should minus off 32 characters.
Because on first run of encrypt, the key_location is already the end of the flag = start + 32 characters.

We can see the wraparound logic:
    if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]

So what we can do is that we do not pass in 50000. If we pass in 50000, observe:
    stop == x + 50000

    This is >= KEY_LEN, so
    
    stop = stop % KEY_LEN # Here stop becomes 0.
    key = kf[start:] + kf[:stop]

    So key = kf[start:] + 0 = kf[start:]

    And do not forget this start is inclusive of the flag's length. Because this is a first run.
    So we should pass in 49 968; this will guarantee a wrap around and be missing on 32 characters,
    hence returning the true index of the start of the key_location as in startup().

Then notice, we will wraparound to the start. We need the actual key: just input in 32 characters.
Then, the output should be an encrypted with the same key as used in startup().

Here, i needed help in syntax-wise on how to execute this; how to create X number of characters and then
pass it into the netcat utility.

Googling search taught me to use the pipe operator and python:

python3 -c "print('a'*49968);print('a'*32)" | nc mercury.picoctf.net 36981

Running this line enables me to first print out the 49968 characters of 'a', then pass
into the server. Then it will do the same with the 32 bits which should be the flag's length

This returns two outputs; we are only interested in the encrypted second output:
0346483f243d1959563d1907563d1903543d190551023d1959073d1902573d19

We were finding for k:
We can XOR twice of the 'a' .... with the key output to get the original key

They here used XOR to find out what k is:
so k^ord('a') 32 times.
So we need to know the hex of ord(a), 32 times it.

Python hex(ord('a')) reveals 0x61.
So we have 0x61616161... 32 times of 61.

So the output we get from 0346483f243d1959563d1907563d1903543d190551023d1959073d1902573d19
This is ord(p) ^ k in hexadecimal, where 32 times of `a`.

In other words:

0346483f243d1959563d1907563d1903543d190551023d1959073d1902573d19
=
`a`*32 ^ (bits of k), bit-wise

Back to our main goal, we need k.
So we can get k by XORing with 0x61.. 32 times:

In Python:
>>> print("0x" + "61"*32)
0x6161616161616161616161616161616161616161616161616161616161616161

...XORing with the output to reveal the key:
>>> 0x6161616161616161616161616161616161616161616161616161616161616161^0x0346483f243d1959563d1907563d1903543d190551023d1959073d1902573d19
44395851709826256090104236678511664613940528955743340129162515544472466906232

So 44395851709826256090104236678511664613940528955743340129162515544472466906232
Is the key's decimal value. Converting it to hexadecimal: 0x6227295e455c7838375c7866375c7862355c786430635c7838665c7863365c78


We will use this to XOR with the encrypted flag:
5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c

>>> 0x6227295e455c7838375c7866375c7862355c786430635c7838665c7863365c78^0x5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c 
25057821178459433675179303676199845791448110008844411929611525408183085850932

This is the plaintext in decimal value: 25057821178459433675179303676199845791448110008844411929611525408183085850932

Converting to hex...
>>> hex(25057821178459433675179303676199845791448110008844411929611525408183085850932)
'0x3766396461323966343034393961393864623232303338306135373734366134'

Then input into a converter online:
'3766396461323966343034393961393864623232303338306135373734366134'
returns 
7f9da29f40499a98db220380a57746a4

Which is the flag: wrapping with picoCTF{...} we get:
picoCTF{7f9da29f40499a98db220380a57746a4}

'''

#!/usr/bin/python3 -u
import os.path

KEY_FILE = "key"
KEY_LEN = 50000
FLAG_FILE = "flag"


def startup(key_location):
	flag = open(FLAG_FILE).read()
	kf = open(KEY_FILE, "rb").read()

	start = key_location
	stop = key_location + len(flag)

	key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), flag, key))
	print("This is the encrypted flag!\n{}\n".format("".join(result)))

	return key_location

def encrypt(key_location):
	ui = input("What data would you like to encrypt? ").rstrip()
	if len(ui) == 0 or len(ui) > KEY_LEN:
		return -1

	start = key_location
	stop = key_location + len(ui)

	kf = open(KEY_FILE, "rb").read()

	if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), ui, key))

	print("Here ya go!\n{}\n".format("".join(result)))

	return key_location


print("******************Welcome to our OTP implementation!******************")
c = startup(0)
while c >= 0:
	c = encrypt(c)
