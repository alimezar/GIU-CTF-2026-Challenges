# CTF Challenge Writeup: Airport

## Challenge Information
- **Name:** Airport
- **Hardness:** Easy
- **Solve Count:** 21
- **Points:** 100

## Solution

### Step 1: Search for how flight tickets works/formatted
Search for what format flight tickets uses for barcodes

### Step 2: Scan the Barcode
Scan the flight ticket to extract the data from the PDF417 barcode

**Recommended Tool:** [Inlite Online Barcode Reader](https://online-barcode-reader.inliteresearch.com/) or similar PDF417 decoders.

Upon scanning, you will receive a string of text.

### Step 3: Decode the IATA Format
The resulting text follows the **IATA (International Air Transport Association)** standard for boarding passes. This format includes fields for the passenger name, flight number, seat, and electronic ticket indicators.

To quickly parse this string and find the flag:
1. Copy the raw output from the scanner.
2. Provide the string to an **AI (like ChatGPT or Gemini)** and ask it to "Explain the IATA encoding and extract hidden data."
3. The AI will break down the segments, revealing the flag hidden within one of the data fields (often the passenger name or flight info).

## Flag
`GIUCTF{A13371337}`
