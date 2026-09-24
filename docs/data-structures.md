# Data Structures

The ParkSmart system uses simple data structures to organize and process parking information.

The main data structures used are:

1. Array/List
2. Queue
3. List

These structures were selected because they are simple and appropriate for the operations required by the parking system.

---

## 1. Array/List

An array-like structure is used to represent the collection of parking slots.

In Python, a standard `list` is used to store the parking slots.

Example:

```text
ParkingSlots = [A1, A2, A3, A4, A5]
```

Each parking slot has a status:

```text
A1 → OCCUPIED
A2 → AVAILABLE
A3 → AVAILABLE
A4 → OCCUPIED
A5 → AVAILABLE
```

The system can go through the slots one by one to find an available parking space.

### Reason for Use

A list is suitable because the parking facility contains a collection of parking slots that need to be checked.

It allows the system to:

- Store multiple parking slots.
- Access individual slots.
- Traverse the slots one by one.
- Find an available slot.

### Basic Complexity

For a Python list:

| Operation | Average Complexity |
|-----------|---------------------|
| Access an element by index | O(1) |
| Search/traverse all slots | O(n) |

Where `n` represents the number of parking slots.

### Example

```python
parking_slots = ["A1", "A2", "A3", "A4", "A5"]

for slot in parking_slots:
    print(slot)
```

The system can check each slot until it finds one that is available.

---

## 2. Queue

A queue is used to store vehicles waiting for a parking slot when the parking area is full.

The queue follows the FIFO (First In, First Out) principle.

Example:

```text
FRONT
  ↓
KDA123A → KCB456B → KDE789C
                         ↑
                        REAR
```

The vehicle that enters the queue first is handled first when a parking slot becomes available.

### Reason for Use

A queue is suitable because vehicles waiting to enter the parking area should be handled in the order in which they arrived.

For example:

```text
Vehicle A arrives first
Vehicle B arrives second
Vehicle C arrives third
```

The order remains:

```text
Vehicle A → Vehicle B → Vehicle C
```

Vehicle A will therefore be served first.

### Python Implementation

Python's `deque` can be used to implement the queue efficiently.

```python
from collections import deque

waiting_queue = deque()
```

Adding a vehicle:

```python
waiting_queue.append(vehicle)
```

Removing the first vehicle:

```python
waiting_queue.popleft()
```

### Basic Complexity

| Operation | Complexity |
|-----------|------------|
| Add item | O(1) |
| Remove first item | O(1) |

The queue therefore provides efficient insertion at the rear and removal from the front.

---

## 3. List

A list can be used when the application needs to temporarily hold or process multiple parking records.

Example:

```text
ParkingRecords

KDA123A | A1 | 08:00
KCB456B | A2 | 08:30
KDE789C | A3 | 09:00
```

The number of parking records changes as vehicles enter and leave the parking facility.

### Reason for Use

A list is suitable for processing a collection of records because:

- Records can be stored together.
- Records can be traversed one by one.
- Records can be searched.
- Records can be added or removed when required.

### Basic Complexity

A simple search through a list takes:

```text
O(n)
```

where `n` is the number of records.

For example, if the system searches for a vehicle's registration number, it may need to examine the records one by one until a matching record is found.

---

## 4. Data Structure Selection

| Data Structure | System Use | Reason |
|------------------|-------------|--------|
| List / Array-like structure | Parking slots | Stores and allows traversal of parking slots |
| Queue | Waiting vehicles | Maintains vehicle arrival order using FIFO |
| List | Temporary parking-record processing | Allows records to be stored, searched and processed |

---

## 5. Relationship Between Data Structures and Algorithms

The selected data structures support the algorithms used by the system.

| Algorithm | Data Structure Used |
|-----------|----------------------|
| Display Parking Availability | List |
| Vehicle Entry | List |
| Find Parking Record | List / database records |
| Calculate Parking Fee | Basic variables |
| Vehicle Exit | Parking records |
| Manage Waiting Queue | Queue |
| Overall Parking Algorithm | Combination of the above |

For example, the Vehicle Entry Algorithm traverses the list of parking slots to find an available slot.
The Waiting Queue Algorithm uses a queue to ensure that vehicles waiting for parking are handled according to the FIFO principle.
The Parking Records Algorithm searches through parking records to find the record belonging to a particular vehicle.

---