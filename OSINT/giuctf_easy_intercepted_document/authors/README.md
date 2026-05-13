# CTF Challenge Writeup: Intercepted Document

## Challenge Information

- **Name:** Intercepted Document
- **Hardness:** Easy-Medium
- **Solve Count:** 14 (Part 1), 8 (Part 2)
- **Points:** 100 (Part 1), 150 (Part 2)

---

## Solution

### Step 1: Extract the PDF Hash

The challenge provides an encrypted PDF document. To begin the cracking process, use the `pdf2john` tool to extract the password hash from the file. This converts the PDF's encryption data into a format that password-cracking tools can recognize.

### Step 2: Crack the PDF Password

Once you have the hash, use **Hashcat** (or John the Ripper) alongside the **rockyou.txt** wordlist to perform a dictionary attack.

### Step 3: Retrieve Flag 1 (Victim Email)

Open the PDF using the cracked password. Inside the document, locate the email address of the victim. This email address serves as the first flag.

### Step 4: Retrieve Flag 2 (Password Leak)

To find the second flag, you must uncover the password associated with the email found in Step 3. You can achieve this using two methods:

1. **Leak Databases:** Use a Credential/Password Leak search engine (such as [proxynova.com](https://api.proxynova.com/comb)) to query the email address.
2. **Hash Cracking:** Alternatively, if a Credential/Password Leak search engine providdes the victim's hashed, it can be cracked using **rockyou.txt**.

The discovered password for the account is the second flag.

---

## Flag

**Flag 1:** `GIUCTF{mangoman0@gmail.com}`

**Flag 2:** `GIUCTF{momopefo}`
