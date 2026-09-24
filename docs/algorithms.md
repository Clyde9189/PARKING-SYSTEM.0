# Algorithms

Each major module of the parking management system has its own algorithm. The algorithms describe the step-by-step procedures used by the system to manage parking availability, vehicle entry, parking records, fee calculation, and vehicle exit.

---

## 1. Parking Availability Algorithm

The Parking Availability Algorithm displays the current status of every parking slot.

**Input**

- List of parking slots
- Status of each parking slot

**Output**

- Parking-slot availability

**Pseudocode**

```text
ALGORITHM DisplayParkingAvailability

START

FOR each parking slot

    IF slot status = AVAILABLE THEN

        Display slot number
        Display "AVAILABLE"

    ELSE

        Display slot number
        Display "OCCUPIED"

    END IF

END FOR

END
```

The algorithm checks each parking slot one at a time.
If the status of a slot is `AVAILABLE`, the system displays the slot number and `AVAILABLE`.
If the status is not available, the system displays the slot number and `OCCUPIED`.
This allows drivers to see which parking slots are currently available before entering the parking area.

---

## 2. Vehicle Entry Algorithm

The Vehicle Entry Algorithm records an arriving vehicle and assigns an available parking slot.

**Input**

- Vehicle registration number
- Vehicle type
- Parking slots
- Current time

**Output**

- Assigned parking slot
- Vehicle entry record

**Pseudocode**

```text
ALGORITHM VehicleEntry

START

Enter vehicle registration number

Enter vehicle type

FOR each parking slot

    IF slot status = AVAILABLE THEN

        Assign slot to vehicle

        Record entry time

        Change slot status to OCCUPIED

        Save parking record

        Display assigned slot

        STOP

    END IF

END FOR

Display "PARKING FULL"

Add vehicle to waiting queue

END
```

The algorithm first receives the vehicle registration number and vehicle type.
It then checks the parking slots one by one. When the first available slot is found, the system assigns the slot to the vehicle, records the entry time, changes the slot status to `OCCUPIED`, and saves the parking record.
If no available slot is found, the system displays `PARKING FULL` and places the vehicle in the waiting queue.
The waiting queue follows the First In, First Out (FIFO) principle.

---

## 3. Parking Records Algorithm

The Parking Records Algorithm searches for the active parking record of a vehicle.

**Input**

- Vehicle registration number
- Parking records

**Output**

- Vehicle parking record
- `VEHICLE NOT FOUND` if no record exists

**Pseudocode**

```text
ALGORITHM FindParkingRecord

START

Enter vehicle registration number

FOR each parking record

    IF record registration number =
       entered registration number THEN

        Return parking record

    END IF

END FOR

Return "VEHICLE NOT FOUND"

END
```

The algorithm searches through the parking records one by one.
For each record, it compares the stored vehicle registration number with the registration number entered by the user.
If a matching record is found, the system returns the parking record.
If no matching record is found after checking all records, the system returns `VEHICLE NOT FOUND`.
This algorithm is used during vehicle exit to identify the correct parking session.

---

## 4. Fee Calculation Algorithm

The Fee Calculation Algorithm calculates the total parking duration and determines the amount payable according to the parking tariff provided by the client.

**Input**

- Entry time
- Exit time

**Output**

- Parking duration
- Amount payable

**Parking Tariff**

| Parking Duration | Fee |
|-------------------|-----|
| Up to 30 minutes | FREE |
| More than 30 minutes up to 2 hours | KSh 50 |
| More than 2 hours up to 4 hours | KSh 100 |
| More than 4 hours up to 6 hours | KSh 300 |
| More than 6 hours | KSh 500 |

**Pseudocode**

```text
ALGORITHM CalculateParkingFee

START

Get entry time

Get exit time

Calculate time difference

Calculate total parking duration in minutes

IF duration <= 30 minutes THEN

    Fee = KSh 0

ELSE IF duration <= 120 minutes THEN

    Fee = KSh 50

ELSE IF duration <= 240 minutes THEN

    Fee = KSh 100

ELSE IF duration <= 360 minutes THEN

    Fee = KSh 300

ELSE

    Fee = KSh 500

END IF

Display parking duration

Display fee

END
```

The algorithm first obtains the vehicle's entry and exit times.
The difference between the two times is calculated to determine the total parking duration in minutes.
The duration is then compared with the parking-fee brackets specified by the client.

For example:

- A vehicle parked for 20 minutes pays KSh 0.
- A vehicle parked for 1 hour pays KSh 50.
- A vehicle parked for 3 hours pays KSh 100.
- A vehicle parked for 5 hours pays KSh 300.
- A vehicle parked for 7 hours pays KSh 500.

The fee is determined by the total parking duration, rather than by multiplying the number of hours by a fixed hourly rate.

---

## 5. Vehicle Exit Algorithm

The Vehicle Exit Algorithm processes a vehicle leaving the parking facility.

**Input**

- Vehicle registration number
- Payment amount

**Output**

- Payment result
- Released parking slot
- Barrier status
- Parking duration
- Amount payable

**Pseudocode**

```text
ALGORITHM VehicleExit

START

Enter vehicle registration number

Search for parking record

IF vehicle is not found THEN

    Display "VEHICLE NOT FOUND"

    Keep barrier CLOSED

    STOP

END IF

Get entry time

Record exit time

Calculate parking duration

Calculate parking fee

Display parking duration

Display amount to pay

Receive payment

IF payment >= amount payable THEN

    Mark payment as successful

    Mark parking slot as AVAILABLE

    Update parking record with exit time

    Display "PAYMENT SUCCESSFUL"

    Display "BARRIER OPEN"

    Open exit barrier

ELSE

    Display "INSUFFICIENT PAYMENT"

    Keep barrier CLOSED

END IF

END
```

The algorithm first receives the vehicle registration number and searches for the vehicle's active parking record.
If no record is found, the system displays `VEHICLE NOT FOUND` and keeps the exit barrier closed.
If the vehicle is found, the system records the exit time and calculates the total parking duration.
The system then calculates the parking fee using the client's tariff.
The required amount is displayed and payment is received.

If the payment is equal to or greater than the required amount:

1. The payment is marked as successful.
2. The parking record is updated.
3. The parking slot is changed to `AVAILABLE`.
4. The exit barrier is opened.

If the payment is insufficient, the barrier remains closed and the vehicle remains in the parking area.

---

## 6. Waiting Queue Algorithm

The Waiting Queue Algorithm manages vehicles when all parking slots are occupied.
The queue uses the First In, First Out (FIFO) principle.

**Input**

- Vehicle information
- Waiting queue

**Output**

- Vehicle added to the waiting queue
- Next vehicle to receive an available slot

**Pseudocode**

```text
ALGORITHM ManageWaitingQueue

START

IF no parking slot is AVAILABLE THEN

    Add arriving vehicle to the end of the queue

    Display "PARKING FULL"

ELSE

    IF waiting queue is not empty THEN

        Remove the first vehicle from the queue

        Assign an available slot to the vehicle

        Record entry time

        Mark slot as OCCUPIED

    END IF

END IF

END
```

When all parking slots are occupied, an arriving vehicle is added to the waiting queue.
The vehicle is placed at the end of the queue.
When a parking slot becomes available, the system serves the vehicle at the front of the queue first.

For example:

```text
Waiting Queue

Front                         Rear
  ↓                             ↓
KCA 101A → KCB 202B → KCC 303C
```

If a parking slot becomes available, `KCA 101A` is served first.

This demonstrates the practical use of a Queue data structure in the parking system.

---

## 7. Overall Algorithm

The complete parking management system can be summarized using the following algorithm.

```text
ALGORITHM ParkingManagementSystem

START

Display parking availability

WAIT for vehicle

IF vehicle arrives THEN

    Record vehicle information

    Check for an available parking slot

    IF slot is available THEN

        Assign available slot

        Record entry time

        Mark slot OCCUPIED

        Save parking record

    ELSE

        Display "PARKING FULL"

        Add vehicle to waiting queue

    END IF

END IF

WAIT for vehicle at exit

IF vehicle arrives at exit THEN

    Search for vehicle parking record

    IF vehicle is found THEN

        Record exit time

        Calculate parking duration

        Calculate parking fee

        Display amount payable

        Receive payment

        IF payment is sufficient THEN

            Mark payment as successful

            Update parking record

            Mark parking slot AVAILABLE

            Open exit barrier

        ELSE

            Display "INSUFFICIENT PAYMENT"

            Keep barrier CLOSED

        END IF

    ELSE

        Display "VEHICLE NOT FOUND"

        Keep barrier CLOSED

    END IF

END IF

END
```
