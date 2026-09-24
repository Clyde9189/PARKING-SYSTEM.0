# Overall System Design

The system follows a simple sequence from vehicle arrival to vehicle exit.

---

## System Process

```text
START
  │
  ▼
Display Parking Availability
  │
  ▼
Vehicle Arrives
  │
  ▼
Check Available Slot
  │
  ├─────────────── NO ───────────────┐
  │                                  │
 YES                                 ▼
  │                            Display "FULL"
  ▼
Record Vehicle
  │
  ▼
Assign Parking Slot
  │
  ▼
Record Entry Time
  │
  ▼
Vehicle Parks
  │
  ▼
Vehicle Arrives at Exit
  │
  ▼
Find Parking Record
  │
  ▼
Record Exit Time
  │
  ▼
Calculate Duration
  │
  ▼
Calculate Fee
  │
  ▼
Process Payment
  │
  ├──────────── FAILED ──────────────┐
  │                                  │
 SUCCESS                             ▼
  │                            Keep Barrier
  ▼                               Closed
Release Parking Slot
  │
  ▼
Update Slot Status
  │
  ▼
Open Exit Barrier
  │
  ▼
END
```

---

## Module Interaction

The modules work together as follows:

```text
Parking Availability
        │
        ▼
Vehicle Entry
        │
        ▼
Parking Records
        │
        ▼
Fee Calculation
        │
        ▼
Vehicle Exit
```

### Parking Availability

Shows the current status of parking slots.

### Vehicle Entry

Records the vehicle and assigns a slot.

### Parking Records

Stores the vehicle's parking information.

### Fee Calculation

Uses entry and exit times to calculate the amount payable.

### Vehicle Exit

Processes payment and releases the vehicle.

---

## Data Structure Interaction

The proposed data structures support the modules as follows:

```text
Array
  │
  └── Parking Slots

Queue
  │
  └── Waiting Vehicles

List
  │
  └── Parking Records
```

---

## Database Interaction

The application interacts with the database during the parking process.

### Vehicle Entry

```text
Vehicle
   ↓
Create/Find Vehicle Record
   ↓
Assign Slot
   ↓
Create Parking Record
   ↓
Update Slot Status
```

### Vehicle Exit

```text
Vehicle
   ↓
Find Parking Record
   ↓
Record Exit Time
   ↓
Calculate Fee
   ↓
Record Amount Paid
   ↓
Update Slot Status
   ↓
Open Barrier
```

---

## Overall System Algorithm

```text
ALGORITHM ParkingSystem

START

Display parking slots

WAIT for vehicle

IF vehicle arrives THEN

    Record vehicle information

    Search for available parking slot

    IF slot is available THEN

        Assign slot

        Record entry time

        Mark slot as OCCUPIED

        Create parking record

    ELSE

        Display "PARKING FULL"

    END IF

END IF

WAIT for vehicle at exit

IF vehicle arrives at exit THEN

    Search for parking record

    IF record exists THEN

        Record exit time

        Calculate parking duration

        Calculate parking fee

        Display amount payable

        Receive payment

        IF payment is successful THEN

            Update parking record

            Mark parking slot AVAILABLE

            Open exit barrier

        ELSE

            Keep exit barrier CLOSED

        END IF

    ELSE

        Display "VEHICLE NOT FOUND"

    END IF

END IF

END
```

---

## Expected System Behaviour

### Scenario 1: Parking Space Available

```text
Vehicle arrives
       ↓
Available slot found
       ↓
Vehicle recorded
       ↓
Slot assigned
       ↓
Entry time recorded
       ↓
Slot becomes OCCUPIED
```

### Scenario 2: Parking Full

```text
Vehicle arrives
       ↓
No available slot
       ↓
Display "PARKING FULL"
       ↓
Vehicle does not enter
```

### Scenario 3: Successful Exit

```text
Vehicle arrives at exit
       ↓
Parking record found
       ↓
Duration calculated
       ↓
Fee calculated
       ↓
Payment successful
       ↓
Slot becomes AVAILABLE
       ↓
Barrier opens
```

### Scenario 4: Failed Payment

```text
Vehicle arrives at exit
       ↓
Fee calculated
       ↓
Payment unsuccessful
       ↓
Barrier remains CLOSED
```