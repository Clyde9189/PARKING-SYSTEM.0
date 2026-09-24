# Dynamic Database Design

The database is used to permanently store information about vehicles, parking slots, and parking activities.

The database is dynamic because its information changes as vehicles enter and leave the parking facility.

For example, when a vehicle enters, a parking slot changes from:

```text
AVAILABLE
```

to:

```text
OCCUPIED
```

When the vehicle leaves, the slot changes back to:

```text
AVAILABLE
```

The database therefore allows the system to maintain up-to-date parking information.

---

## Database Entities

The proposed database contains three main entities:

1. Vehicles
2. Parking Slots
3. Parking Records

---

## 1. Vehicles Table

The `vehicles` table stores information about vehicles using the parking facility.

| Field | Data Type | Description |
|-------|-----------|--------------|
| `vehicle_id` | INTEGER | Unique vehicle ID |
| `registration_number` | TEXT | Vehicle registration number |
| `vehicle_type` | TEXT | Type of vehicle |

### Example

| vehicle_id | registration_number | vehicle_type |
|------------|----------------------|---------------|
| 1 | KDA123A | Car |
| 2 | KCB456B | SUV |
| 3 | KDE789C | Van |

The `vehicle_id` is the Primary Key (PK) and uniquely identifies each vehicle.
The `registration_number` is also unique so that the same registration number cannot be entered twice as a separate vehicle.

---

## 2. Parking Slots Table

The `parking_slots` table stores information about the parking spaces.

| Field | Data Type | Description |
|-------|-----------|--------------|
| `slot_id` | INTEGER | Unique slot ID |
| `slot_number` | TEXT | Parking slot number |
| `status` | TEXT | Available or occupied |

### Example

| slot_id | slot_number | status |
|---------|--------------|--------|
| 1 | A1 | OCCUPIED |
| 2 | A2 | AVAILABLE |
| 3 | A3 | AVAILABLE |
| 4 | A4 | OCCUPIED |

The `slot_id` is the Primary Key.
The `slot_number` uniquely identifies the physical parking space.
The `status` records whether the slot is currently available or occupied.

---

## 3. Parking Records Table

The `parking_records` table stores information about each vehicle's parking session.

| Field | Data Type | Description |
|-------|-----------|--------------|
| `record_id` | INTEGER | Unique parking record |
| `vehicle_id` | INTEGER | Vehicle reference |
| `slot_id` | INTEGER | Parking slot reference |
| `entry_time` | TEXT | Vehicle entry time |
| `exit_time` | TEXT | Vehicle exit time |
| `duration` | INTEGER | Parking duration in minutes |
| `amount_paid` | REAL | Amount paid |

The `record_id` is the Primary Key.
`vehicle_id` and `slot_id` are Foreign Keys (FKs) that connect the parking record to the vehicle and parking slot.
The `exit_time`, `duration`, and `amount_paid` can initially be empty because they are only known when the vehicle exits.

---

## 4. Database Relationships

The relationships between the tables are:

```text
VEHICLES
    │
    │ 1
    │
    │ M
    ▼
PARKING_RECORDS
    │
    │ M
    │
    │ 1
    ▼
PARKING_SLOTS
```

- One vehicle can have many parking records over time.
- One parking slot can be used by many vehicles at different times.
- Each parking record belongs to one vehicle.
- Each parking record uses one parking slot.
- The `parking_records` table connects vehicles and parking slots for each parking session.

For example:

```text
Vehicle KDA123A
       │
       ▼
Parking Record #1
       │
       ▼
Slot A1
```

If the same vehicle returns later, a new parking record can be created.

---

## 5. Entity Relationship Diagram

The basic ERD is:

```text
┌──────────────────────────┐
│         VEHICLES         │
├──────────────────────────┤
│ PK vehicle_id            │
│ registration_number      │
│ vehicle_type             │
└────────────┬─────────────┘
             │
             │ 1
             │
             │ M
             ▼
┌──────────────────────────┐
│     PARKING_RECORDS      │
├──────────────────────────┤
│ PK record_id             │
│ FK vehicle_id            │
│ FK slot_id               │
│ entry_time               │
│ exit_time                │
│ duration                 │
│ amount_paid              │
└────────────┬─────────────┘
             │
             │ M
             │
             │ 1
             ▼
┌──────────────────────────┐
│      PARKING_SLOTS       │
├──────────────────────────┤
│ PK slot_id               │
│ slot_number               │
│ status                   │
└──────────────────────────┘
```

---

## 6. Dynamic Database Operation

### When a Vehicle Enters

Suppose vehicle `KDA123A` enters and is assigned parking slot `A1`.

A new parking record is created:

```text
Vehicle: KDA123A
Slot: A1
Entry Time: 08:00
Exit Time: NULL
Duration: NULL
Amount Paid: NULL
```

The parking slot is then updated:

```text
A1 → OCCUPIED
```

The database now contains an active parking session for the vehicle.

### When the Vehicle Exits

Suppose vehicle `KDA123A` entered at 08:00 and leaves at 11:00.

The total parking duration is:

```text
3 hours = 180 minutes
```

According to the client's tariff, a parking duration of up to 4 hours costs:

```text
KSh 100
```

The parking record is therefore updated to:

```text
Vehicle: KDA123A
Slot: A1
Entry Time: 08:00
Exit Time: 11:00
Duration: 180 minutes
Amount Paid: KSh 100
```

The parking slot is then updated:

```text
A1 → AVAILABLE
```

This demonstrates how the database changes as vehicles enter and leave the parking facility.

---

## 7. Parking Fee Information

The database stores the amount paid for each completed parking session.

The fee is calculated by the Fee Calculation Algorithm before the parking record is completed.

The system uses the following tariff:

| Parking Duration | Fee |
|-------------------|-----|
| Up to 30 minutes | KSh 0 |
| More than 30 minutes up to 2 hours | KSh 50 |
| More than 2 hours up to 4 hours | KSh 100 |
| More than 4 hours up to 6 hours | KSh 300 |
| More than 6 hours | KSh 500 |

The database does not calculate the fee itself. Instead:

```text
Entry Time
     ↓
Exit Time
     ↓
Calculate Duration
     ↓
Calculate Fee
     ↓
Store Amount Paid
```

This separates the database storage responsibility from the application's calculation logic.

---

## 8. Simple Database Schema

The ParkSmart KE system uses SQLite as its database.

The database schema is:

```sql
CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL
);

CREATE TABLE parking_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_number TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL
);

CREATE TABLE parking_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    entry_time TEXT NOT NULL,
    exit_time TEXT,
    duration INTEGER,
    amount_paid REAL,
    FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (slot_id)
        REFERENCES parking_slots(slot_id)
);
```

---

## 9. Database Operations

The system performs basic database operations during normal operation.

### Vehicle Entry

When a vehicle enters:

```text
1. Check whether vehicle exists.
2. Find an available parking slot.
3. Create or retrieve vehicle information.
4. Create a parking record.
5. Change the slot status to OCCUPIED.
```

### Vehicle Exit

When a vehicle exits:

```text
1. Find the vehicle's active parking record.
2. Record the exit time.
3. Calculate the parking duration.
4. Calculate the parking fee.
5. Record the amount paid.
6. Update the parking record.
7. Change the slot status to AVAILABLE.
```

These operations make the database dynamic because records and slot statuses change as the system is used.

---