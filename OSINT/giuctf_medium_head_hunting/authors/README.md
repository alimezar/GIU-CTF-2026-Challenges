# CTF Challenge Writeup: Head Hunting

## Challenge Information

**Name:** Head Hunting
**Hardness:** Medium
**Solve Count:** 0
**Points:** 250

## Solution

### Step 1: Domain Keyword Search
Begin by using the **Domain Keyword Search** feature on [Whoxy](https://www.whoxy.com/). Search for the keyword `webapphackademy`.

### Step 2: Identify the Registrar
Review the domain records for the results. The WHOIS history/record will reveal that **Dafydd Stuttard** was the last registrar associated with this domain.

### Step 3: OSINT Investigation
Perform a simple Google search for "Dafydd Stuttard". The search results confirm that he is the **CEO of PortSwigger**.

### Step 4: Find the Target Domains
Returning to Whoxy, investigate the other domains registered by Dafydd Stuttard. You can identify the primary domain for his company and the latest website that he registered.

## Flag

`GIUCTF{portswigger.net,burpsuite.ai}`
