# ParkSmart: Parking Management System

### Data Structures and Algorithms (Task 1)

A simple web-based automated parking management system developed using Python, Flask, and SQLite.

The system is designed to help a parking facility manage parking-space availability, vehicle entry, parking records, fee calculation, payment, and vehicle exit.

The project focuses on applying Data Structures and Algorithms concepts to solve a practical parking-management problem.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [System Requirements](#️-system-requirements)
- [Parking Tariff](#-parking-tariff)
- [System Modules](#-system-modules)
- [Algorithms](#-algorithms)
- [Data Structures](#️-data-structures)
- [Database Design](#️-database-design)
- [Technology Stack](#️-technology-stack)
- [System Flow](#-system-flow)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Activating the Virtual Environment](#-activating-the-virtual-environment)
- [Running the System](#️-running-the-system)
- [System Demonstration](#-system-demonstration)
- [Barrier Simulation](#-barrier-simulation)
- [Project Scope](#-project-scope)

---

## Project Overview

The proposed system allows drivers to see available parking slots before entering the parking area.

When a vehicle arrives, the system:

1. Records the vehicle registration number.
2. Records the vehicle type.
3. Searches for an available parking slot.
4. Assigns an available slot.
5. Records the vehicle's entry time.
6. Marks the parking slot as occupied.

When the vehicle leaves, the system:

1. Identifies the vehicle using its registration number.
2. Records the exit time.
3. Calculates the total parking duration.
4. Calculates the parking fee.
5. Receives payment.
6. Checks whether the payment is sufficient.
7. Makes the parking slot available again.
8. Opens the exit barrier after successful payment.

If the parking area is full, arriving vehicles are placed in a FIFO waiting queue.

The project focuses on implementing the client's requirements using simple and appropriate Data Structures, Algorithms, and a Dynamic Database.

---

## Objectives

### General Objective

To develop a simple automated parking management system using appropriate algorithms, data structures, and a dynamic database.

### Specific Objectives

The system should:

1. Display available parking slots.
2. Show whether each parking slot is available or occupied.
3. Record vehicles when they arrive.
4. Assign available parking slots.
5. Record vehicle entry time.
6. Keep track of parked vehicles.
7. Record vehicle exit time.
8. Calculate parking duration.
9. Calculate the parking fee.
10. Process payment at exit.
11. Open the exit barrier after successful payment.
12. Keep the barrier closed when payment is insufficient.
13. Make the parking slot available after the vehicle exits.
14. Store parking information in a database.
15. Maintain a waiting queue when all parking slots are occupied.

---

## System Requirements

### Functional Requirements

| | Requirements |
|----|-------------|
| 1 | Display parking slot availability |
| 2 | Show whether each slot is available or occupied |
| 3 | Record vehicle information on arrival |
| 4 | Assign an available parking slot |
| 5 | Record vehicle entry time |
| 6 | Keep track of parked vehicles |
| 7 | Record vehicle exit time |
| 8 | Calculate parking duration |
| 9 | Calculate parking fee |
| 10 | Process payment |
| 11 | Keep barrier closed when payment is insufficient |
| 12 | Open barrier after successful payment |
| 13 | Make the parking slot available after exit |
| 14 | Store parking records in a database |
| 15 | Maintain a waiting queue when parking is full |

---

## Parking Tariff

The system uses the parking fees provided in the assignment.

| Parking Duration | Fee |
|-------------------|-----|
| Up to 30 minutes | FREE |
| Up to 2 hours | KSh 50 |
| Up to 4 hours | KSh 100 |
| Up to 6 hours | KSh 300 |
| Over 6 hours | KSh 500 |

### Fee Calculation Examples

| Parking Time | Amount |
|--------------|--------|
| 20 minutes | FREE |
| 30 minutes | FREE |
| 1 hour | KSh 50 |
| 2 hours | KSh 50 |
| 2 hours 30 minutes | KSh 100 |
| 4 hours | KSh 100 |
| 5 hours | KSh 300 |
| 6 hours | KSh 300 |
| 7 hours | KSh 500 |

The system determines the fee using the total elapsed parking time.

---

## System Modules

The system is divided into five main modules.

### 1. Parking Availability Module

Responsible for displaying all parking slots and their current status.

Each slot can have one of two states:

- `AVAILABLE`
- `OCCUPIED`

### 2. Vehicle Entry Module

Responsible for:

- Receiving vehicle registration number.
- Receiving vehicle type.
- Finding an available parking slot.
- Assigning the slot.
- Recording entry time.
- Marking the slot as occupied.

If no slot is available, the vehicle is placed in the waiting queue.

### 3. Parking Records Module

Responsible for maintaining information about parking sessions.

A parking record contains:

- Vehicle
- Parking slot
- Entry time
- Exit time
- Duration
- Amount paid

### 4. Fee Calculation Module

Responsible for:

- Calculating parking duration.
- Determining the correct tariff.
- Calculating the amount payable.

The module follows the client's specified parking tariff.

### 5. Vehicle Exit Module

Responsible for:

- Finding the vehicle's parking record.
- Recording exit time.
- Calculating parking duration.
- Calculating the parking fee.
- Checking payment.
- Releasing the parking slot.
- Opening the barrier after successful payment.

Detailed module documentation can be found in:
`docs/system-modules.md`

---

## Algorithms

An algorithm is developed for each major operation in the system.

The main algorithms are:

1. Parking Availability Algorithm
2. Vehicle Entry Algorithm
3. Parking Record Search Algorithm
4. Fee Calculation Algorithm
5. Vehicle Exit Algorithm
6. Waiting Queue Algorithm

The algorithms are implemented in `app.py` and documented in:
`docs/algorithms.md`

---

## Data Structures

The system uses simple data structures appropriate for the problem.

| Data Structure | Purpose |
|-----------------|---------|
| List | Represents collections such as parking slots when processed by the application |
| Queue | Stores vehicles waiting for an available parking slot |

### Queue

The waiting queue follows the FIFO principle:

**First In, First Out**

For example:

```text
Vehicle A → Vehicle B → Vehicle C
    ↓
Vehicle A is served first
```

Python's `deque` is used to implement the waiting queue.

Detailed information can be found in:
`docs/data-structures.md`

---

## Database Design

The system uses SQLite as its dynamic database.

Three main tables are used:

### 1. `vehicles`

Stores information about vehicles.

```text
vehicle_id
registration_number
vehicle_type
```

### 2. `parking_slots`

Stores information about parking spaces.

```text
slot_id
slot_number
status
```

### 3. `parking_records`

Stores parking sessions.

```text
record_id
vehicle_id
slot_id
entry_time
exit_time
duration
amount_paid
```

### Database Relationships

```text
VEHICLES
   |
   | 1
   |
   | Many
PARKING_RECORDS
   |
   | Many
   |
   | 1
PARKING_SLOTS
```

A vehicle can have multiple parking records over time.
A parking slot can also be used by different vehicles at different times.
The `parking_records` table connects the vehicle and parking slot for each parking session.

The database design is documented in:
`docs/database-design.md`

The SQL schema is available in:
`schema.sql`

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Flask | Web framework |
| SQLite | Dynamic database |
| HTML | Web interface |
| CSS | Interface styling |
| Jinja2 | Dynamic HTML templates |

---

## System Flow

```text
                    START
                      |
                      ↓
             Display Parking Slots
                      |
                      ↓
                Vehicle Arrives
                      |
                      ↓
             Is Slot Available?
                 /          \
               No            Yes
               |              |
               ↓              ↓
        Add Vehicle to   Record Vehicle
        Waiting Queue         |
                              ↓
                         Assign Slot
                              |
                              ↓
                       Record Entry Time
                              |
                              ↓
                       Mark Slot Occupied
                              |
                              ↓
                        Vehicle Parks
                              |
                              ↓
                        Vehicle Exits
                              |
                              ↓
                    Find Parking Record
                              |
                              ↓
                     Record Exit Time
                              |
                              ↓
                   Calculate Duration
                              |
                              ↓
                      Calculate Fee
                              |
                              ↓
                         Payment
                       /         \
                     Fail       Success
                      |            |
                      ↓            ↓
               Keep Barrier    Update Record
                  Closed            |
                                   ↓
                            Release Parking Slot
                                   |
                                   ↓
                             Open Barrier
                                   |
                                   ↓
                                  END
```

---

## Project Structure

```text
parking-system-dsa/
│
├── README.md
├── app.py
├── requirements.txt
├── schema.sql
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── docs/
    ├── requirements-analysis.md
    ├── system-modules.md
    ├── algorithms.md
    ├── data-structures.md
    ├── database-design.md
    ├── system-design.md
```

### File Descriptions

| File/Folder | Purpose |
|--------------|---------|
| `app.py` | Main Flask application and system logic |
| `requirements.txt` | Python dependencies |
| `schema.sql` | Database table definitions |
| `templates/index.html` | Web interface |
| `static/style.css` | Web interface styling |
| `docs/` | Project analysis and design documentation |
| `README.md` | Project overview and setup instructions |
| `.gitignore` | Files excluded from Git |

---

## Installation and Setup

### Prerequisites

Before running the system, make sure Python is installed.

Check the Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

The project requires Python 3.

### 1. Clone the Repository

If the project is already on GitHub, clone it using:

```bash
git clone <repository-url>
```

Then move into the project directory:

```bash
cd parking-system-dsa
```

### 2. Create a Virtual Environment

A virtual environment keeps the project's Python packages separate from other Python projects.

Run:

```bash
python -m venv venv
```

If your system uses `python3`:

```bash
python3 -m venv venv
```

This creates:

```text
venv/
```

inside the project directory.

---

## Activating the Virtual Environment

### Linux / macOS

Run:

```bash
source venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(venv) user@computer:~/parking-system-dsa$
```

### Windows Command Prompt

Run:

```cmd
venv\Scripts\activate
```

You should see:

```text
(venv) C:\parking-system-dsa>
```

### Windows PowerShell

Run:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell prevents the script from running, you may need to allow local scripts for your user account:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
venv\Scripts\Activate.ps1
```

---

## Installing Dependencies

Once the virtual environment has been activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

The project currently requires:

```text
Flask==3.1.2
```

---

## Running the System

After activating the virtual environment and installing the dependencies, run:

```bash
python app.py
```

You should see something similar to:

```text
* Running on http://127.0.0.1:5000
```

Open a web browser and visit:

```text
http://127.0.0.1:5000
```

The ParkSmart KE dashboard should appear.

### Stopping the System

To stop the Flask development server, press:

```text
CTRL + C
```

---


## System Demonstration

The following sequence can be used when demonstrating the project to the lecturer.

### Step 1: Open the Dashboard

The system displays the parking slots.

For example:

```text
A1   A2   A3   A4
FREE FREE FREE FREE

A5   A6   A7   A8
FREE FREE FREE FREE

A9   A10  A11  A12
FREE FREE FREE FREE
```

### Step 2: Register a Vehicle

Enter:

```text
Registration Number: KDA 123A
Vehicle Type: Car
```

Click:

```text
Record Entry
```

The system searches for an available slot.

The first available slot is assigned:

```text
KDA 123A → A1
```

The system then records the entry time.

### Step 3: Check Parking Availability

The dashboard changes:

```text
A1   A2   A3   A4
BUSY FREE FREE FREE
```

The number of available and occupied slots is also updated.

### Step 4: Vehicle Exit

Enter:

```text
Registration Number: KDA 123A
```

Enter the payment amount.

The system:

```text
Find vehicle
     ↓
Find parking record
     ↓
Record exit time
     ↓
Calculate duration
     ↓
Calculate fee
     ↓
Check payment
```

### Step 5: Successful Payment

If the payment is sufficient:

```text
Payment successful.

Barrier OPEN —
vehicle KDA 123A may exit.
```

The parking slot changes from:

```text
OCCUPIED
```

to:

```text
AVAILABLE
```

### Step 6: Insufficient Payment

If the payment is insufficient:

```text
Payment insufficient.

Barrier remains closed.
```

The vehicle remains parked and its parking record is not completed.

---

## Barrier Simulation

The assignment requires the system to open a barrier after successful payment.

Since this is a software-based academic project, a physical barrier is simulated by the system.

After successful payment, the system displays:

```text
Barrier OPEN —
vehicle may exit.
```

When payment is insufficient, it displays:

```text
Barrier remains closed.
```

No physical gate hardware or IoT device is required for this implementation.

---

## Project Scope

The system intentionally focuses on the requirements specified in the assignment.

The following advanced features are outside the scope of this project:

- User authentication
- M-Pesa API integration
- Online payment gateways
- Automatic Number Plate Recognition (ANPR)
- IoT parking sensors
- Physical barrier hardware
- Cloud deployment
- Microservices
- React frontend
- Node.js backend
- Real-time WebSocket communication
- Advanced database servers

These features could be added to a production system, but they are not necessary for demonstrating the Data Structures and Algorithms concepts required by this assignment.

---

## Academic Focus

The project demonstrates the relationship between:

```text
Client Requirements
        ↓
System Modules
        ↓
Algorithms
        ↓
Data Structures
        ↓
Database
        ↓
Python Implementation
        ↓
Web Interface
```

The implementation demonstrates practical use of:

- Arrays/Lists
- Queues
- Searching
- Conditional statements
- Iteration
- Database operations
- Time calculations
- Basic algorithm design

The objective is to solve the parking problem with a simple, understandable implementation appropriate for a second-year Data Structures and Algorithms course.

---

## Documentation

Additional documentation is available in the `docs` directory.

| Document | Description |
|----------|-------------|
| `requirements-analysis.md` | Analysis of the client's requirements |
| `system-modules.md` | Description of the five system modules |
| `algorithms.md` | Algorithms and pseudocode |
| `data-structures.md` | Data structures and reasons for their use |
| `database-design.md` | Dynamic database design |
| `system-design.md` | Overall system design and system flow |

---

## Project

- **Project:** ParkSmart
- **Course:** Data Structures and Algorithms
- **Task:** Task 1
- **Language:** Python
- **Framework:** Flask
- **Database:** SQLite