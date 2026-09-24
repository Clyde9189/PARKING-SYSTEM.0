# System Modules

Each module is responsible fror a specific part of the parking process.

```text
Parking Availability
        ↓
Vehicle Entry
        ↓
Parking Records
        ↓
Fee Calculation
        ↓
Vehicle Exit
```

---

## 1. Parking Availability Module

This module allows drivers to see which parking slots are available before entering the parking facility.

### Inputs

* Parking slot numbers
* Parking slot status

### Processing

System checks each parking slot and determines whether it is available or occupied.

### Output

System displays the status of each parking slot.

Example:
 
```text
A1 - OCCUPIED
A2 - AVAILABLE
A3 - AVAILABLE
A4 - OCCUPIED
A5 - AVAILABLE
```

---

## 2. Vehicle Entry Module

This module records an arriving vehicle and assigns an available parking slot.

### Inputs

* Vehicle registration number
* Vehicle type
* Current date and time
* Available parking slots

### Processing

1. Read vehicle information.
2. Check whether a parking slot is available.
3. Find the first available slot.
4. Assign the slot to the vehicle.
5. Record the entry time.
6. Change the slot status to `OCCUPIED`.

### Output
 
The system provides the assigned parking slot.
 
Example:
 
```text
Vehicle: KDA123A
Assigned Slot: A2
Entry Time: 08:00
```
 
If no slot is available:
 
```text
PARKING FULL
```

---

## 3. Parking Records Module

This module keeps information about vehicles currently parked.

### Stored Info

* Vehicle registration number
* Vehicle type
* Parking slot
* Entry time

Example:
 
```text
KDA123A | Car | A2 | 08:00
KCB456B | SUV  | A3 | 08:30
```
 
### Processing
 
When a vehicle enters, a parking record is created.
 
When a vehicle exits, the corresponding parking record is used to calculate the parking fee and is then removed or marked as completed.

---

## 4. Fee Calculation Module

This module calculates how long a vehicle has stayed in the parking area and determines the amount to be paid.

### Inputs

* Entry time
* Exit time
* Parking rate

### Processing
 
The system:
 
1. Retrieves the entry time.
2. Records the exit time.
3. Calculates the duration.
4. Determines the number of billable hours.
5. Calculates the fee.

## 5. Vehicle Exit Module

This module handles the process of a vehicle leaving the parking facility.

### Inputs

* Vehicle registration number
* Entry time
* Exit time
* Payment

### Processing
 
1. Identify the vehicle.
2. Find its parking record.
3. Record the exit time.
4. Calculate the parking duration.
5. Calculate the amount payable.
6. Receive payment.
7. Verify payment.
8. Release the parking slot.
9. Open the exit barrier.

### Output
 
If payment is successful:
 
```text
Payment Successful
Parking Slot Released
Barrier Open
```
 
If payment fails:
 
```text
Payment Failed
Barrier Remains Closed
```