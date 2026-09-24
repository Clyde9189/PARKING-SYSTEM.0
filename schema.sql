CREATE TABLE IF NOT EXISTS parking_rates (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    minimum_minutes INTEGER NOT NULL,
    maximum_minutes INTEGER,
    amount INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);-- The database contains three main tables:
--
-- 1. vehicles
-- 2. parking_slots
-- 3. parking_records

-- Vehicles Table
CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL
);


-- Parking Slots Table

CREATE TABLE parking_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_number TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'AVAILABLE'
);

-- Parking records table

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