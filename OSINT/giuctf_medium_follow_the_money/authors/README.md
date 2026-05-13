# CTF Challenge Writeup: Follow the Money

## Challenge Information

- **Name:** Follow the Money
- **Hardness:** Medium
- **Solve Count:** 8
- **Points:** 250

---

## Solution

### Step 1: Blockchain Analysis

Start by using a Bitcoin chain analyzer like [Arkham Intelligence](https://www.google.com/search?q=https://intel.arkhamintelligence.com/) or any standard blockchain explorer. Search for the following Bitcoin address:
`3BVswASbgsWcLRLK6qQyU2yhK8YFQt6MHe`

### Step 2: Trace the Inflow

Analyze the transaction history of the address. You will observe that there is only **one inflow transaction**. Trace this transaction back to the sending address:
`38r5HQigv4Yh5ETwhYV8HwZwBbvThwSmfH`

### Step 3: OSINT and Google Dorking

Use a Google Dork to investigate the sending address. Search for the address in quotes or combine it with keywords like "report" or "threat actor."

* **Query:** `"38r5HQigv4Yh5ETwhYV8HwZwBbvThwSmfH"`

This search leads to a technical report published by **Group-IB**, which links this specific wallet address to malicious activity conducted by the **Lazarus Group**.

### Step 4: Extract Operation Details

Review the Group-IB report carefully. It details a specific campaign involving cryptocurrency. Within the text, you will find:

* The **Operation Name**: BTC Changer
* The **Compromised .net Website**: darvishkhan.net

---

## Flag

`GIUCTF{Lazarus_BTC_Changer_darvishkhan.net}`
