# CTF Challenge Writeup: SOCMINT

## Challenge Information

- **Name:** SOCMINT
- **Hardness:** HARD
- **Solve Count:** 19
- **Points:** 300

---

## Solution

### Step 1: Locate the Target Account

Begin by navigating to the Discord profile for the user **"0xchilli"**.

### Step 2: Extract the Discord User ID

1. Right-click the user's **avatar/profile image**.
2. Select **"Open Link in New Tab"** (or "Copy Link").
3. Examine the URL of the image. The numerical string appearing immediately after the `/avatars/` segment is the user's unique **Discord ID**.

### Step 3: Lookup Account Metadata

Once you have the ID, use a Discord lookup tool (such as [discorder.tools](https://discorder.tools/discord-id-lookup/)) to query the account information. These tools parse the ID to reveal the exact timestamp the account was generated on Discord's servers.

The tool will display the **account creation date and time**, which serves as the flag.

---

## Flag

`GIUCTF{11/08/2018_12:23_PM}`
