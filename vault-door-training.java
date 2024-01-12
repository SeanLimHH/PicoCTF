/*
https://play.picoctf.org/practice/challenge/7?page=2

Description
Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints for his Doomsday Project.
The laboratory is protected by a series of locked vault doors.
Each door is controlled by a computer and requires a password to open.
Unfortunately, our undercover agents have not been able to obtain the secret passwords for the vault doors,
but one of our junior agents obtained the source code for each vault's computer!
You will need to read the source code for each level to figure out what the password is for that vault door.
As a warmup, we have created a replica vault in our training facility.
The source code for the training vault is here: VaultDoorTraining.java

The attached file has the following code:

import java.util.*;

class VaultDoorTraining {
    public static void main(String args[]) {
        VaultDoorTraining vaultDoor = new VaultDoorTraining();
        Scanner scanner = new Scanner(System.in); 
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
	if (vaultDoor.checkPassword(input)) {
        System.out.println("Access granted.");
	} else {
        System.out.println("Access denied!");
	}
}

    // The password is below. Is it safe to put the password in the source code?
    // What if somebody stole our source code? Then they would know what our
    // password is. Hmm... I will think of some ways to improve the security
    // on the other doors.
    //
    // -Minion #9567
    public boolean checkPassword(String password) {
        return password.equals("w4rm1ng_Up_w1tH_jAv4_3808d338b46");
    }
}

Solution:

Here we can see that the author put in the password in the challenge. This means, i can immediately
see the password:
w4rm1ng_Up_w1tH_jAv4_3808d338b46

and the flag is thus 
picoCTF{w4rm1ng_Up_w1tH_jAv4_3808d338b46}.

As to how to prevent this: the password should always be kept somewhere else.
In a client and server, this means the client should never have a chance to see
any forms of hashed password if possible. The user just submits a plaintext and the
client should encrypt the plaintext before sending over the internet to the server

The server uses the same encryption algorithm to decrypt the encrypted text.
This way, the user will not know any forms of password and cannot guess that easily other
than its own plaintext-hash.

Encryption is required by the client-side to prevent eavesdropping by other people
monitoring the communication between the client and server.
*/


import java.util.*;

class VaultDoorTraining {
    public static void main(String args[]) {
        VaultDoorTraining vaultDoor = new VaultDoorTraining();
        Scanner scanner = new Scanner(System.in); 
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
	if (vaultDoor.checkPassword(input)) {
	    System.out.println("Access granted.");
	} else {
	    System.out.println("Access denied!");
	}
   }

    // The password is below. Is it safe to put the password in the source code?
    // What if somebody stole our source code? Then they would know what our
    // password is. Hmm... I will think of some ways to improve the security
    // on the other doors.
    //
    // -Minion #9567
    public boolean checkPassword(String password) {
        return password.equals("w4rm1ng_Up_w1tH_jAv4_3808d338b46");
    }
}
