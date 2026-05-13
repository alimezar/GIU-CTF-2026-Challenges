# CTF Challenge Writeup: Accidents Happen

## Challenge Information

- **Name:** Accidents Happen
- **Hardness:** Easy
-  **Solve Count:** 7
- **Points:** 150

---

## Solution

### Step 1: License Plate Search

Start by identifying the **four visible numbers** on the license plate from the provided challenge image. Navigate to [PlatesMania](https://platesmania.com/), a vehicle plate database, and use their search feature to look up those specific digits.

### Step 2: Match the Vehicle

Filter through the search results to find a vehicle that matches the visual characteristics (make, model, color, and surroundings) of the bus shown in the challenge image.

### Step 3: Identify the Bus ID

Once the correct vehicle entry is found on PlatesMania, examine the high-resolution photo. Look closely at the **front glass** of the bus, where the unique **Bus ID** is displayed. Combining the tour operator name visible on the bus with this ID reveals the final flag.

---

## Flag

`GIUCTF{Tez_Tour_98}`
