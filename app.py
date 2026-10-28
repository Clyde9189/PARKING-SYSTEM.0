"""
Main modules:
1. Parking Availability
2. Vehicle Entry
3. Parking Records
4. Fee Calculation
5. Vehicle Exit

Simple data structures:
- List: parking slots returned from the database
- Queue: vehicles waiting when the parking area is full

Database:
- vehicles
- parking_slots
- parking_records
"""
import os
from collections import deque
from datetime import datetime
from math import ceil
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

# app configuration

app = Flask(__name__)

app.secret_key = "parking-system-dsa"

DATABASE = os.environ.get("DATABASE_PATH", "parking.db")

# Number of parking spaces in the demonstration system.
TOTAL_SLOTS = 12


# deque is being used as a FIFO queue.
#
# FIFO = First In, First Out
#
# If the parking area is full, vehicles are placed here.
waiting_queue = deque()

# database functions

def get_db():
    """
    Opens a connection with SQLite database.

    """

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection

def initialize_database():
    """
    Create the database tables.

    Tables created:

    1. vehicles
    2. parking_slots
    3. parking_records
    """

    connection = get_db()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT NOT NULL UNIQUE,
            vehicle_type TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS parking_slots (
            slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'AVAILABLE'
        );

        CREATE TABLE IF NOT EXISTS parking_records (
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

        CREATE TABLE IF NOT EXISTS parking_rates (
            rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            minimum_minutes INTEGER NOT NULL,
            maximum_minutes INTEGER,
            amount REAL NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER NOT NULL UNIQUE,
            amount_due REAL NOT NULL,
            amount_received REAL NOT NULL,
            change_given REAL NOT NULL DEFAULT 0,
            payment_method TEXT NOT NULL,
            transaction_reference TEXT,
            payment_status TEXT NOT NULL,
            paid_at TEXT NOT NULL,
            vat_rate REAL NOT NULL DEFAULT 16,
            vat_amount REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (record_id)
                REFERENCES parking_records(record_id)
        );
    """)

    # Checks whether parking slots already exist.
    count = connection.execute(
        "SELECT COUNT(*) AS count FROM parking_slots"
    ).fetchone()["count"]

    # If no slots exist, create A1 to A12.
    if count == 0:

        for number in range(1, TOTAL_SLOTS + 1):

            connection.execute(
                """
                INSERT INTO parking_slots
                (slot_number, status)
                VALUES (?, ?)
                """,
                (f"A{number}", "AVAILABLE")
            )

    rate_count = connection.execute(
        "SELECT COUNT(*) AS count FROM parking_rates"
    ).fetchone()["count"]

    if rate_count == 0:
        now = datetime.now().isoformat(timespec="seconds")
        default_rates = [
            (0, 30, 0),
            (31, 120, 50),
            (121, 240, 100),
            (241, 360, 300),
            (361, None, 500),
        ]

        for minimum, maximum, amount in default_rates:
            connection.execute(
                """
                INSERT INTO parking_rates
                (minimum_minutes, maximum_minutes, amount, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (minimum, maximum, amount, now, now)
            )

    connection.commit()

    connection.close()

# parking availability

def get_slots():
    """
    Retrieve all parking slots.

    The result displays the current parking availability.
    """

    connection = get_db()

    slots = connection.execute(
        """
        SELECT *
        FROM parking_slots
        ORDER BY slot_id
        """
    ).fetchall()

    connection.close()

    return slots


def find_available_slot():
    """
    vehicle entry algorithm

    Search the parking slots from the first slot to the last.

    The first available slot is returned.

    If no slot is available, None is returned.
    """

    connection = get_db()

    slot = connection.execute(
        """
        SELECT *
        FROM parking_slots
        WHERE status = 'AVAILABLE'
        ORDER BY slot_id
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    return slot


# fee calculation module

def calculate_fee(entry_time, exit_time):
    """
    Calculate parking duration and parking fee.

    Rates:

    Up to 30 minutes:
        FREE

    Up to 2 hours:
        KSh 50

    Up to 4 hours:
        KSh 100

    Up to 6 hours:
        KSh 300

    Over 6 hours:
        KSh 500
    """

    # Calculate total number of seconds.
    elapsed_seconds = (
        exit_time - entry_time
    ).total_seconds()

    # Convert seconds into minutes.
    #
    # ceil() ensures that a partial minute is counted
    # as a complete minute.
    minutes = max(
        0,
        ceil(elapsed_seconds / 60)
    )

    connection = get_db()
    rate = connection.execute(
        """
        SELECT amount
        FROM parking_rates
        WHERE active = 1
          AND minimum_minutes <= ?
          AND (maximum_minutes IS NULL OR maximum_minutes >= ?)
        ORDER BY minimum_minutes DESC
        LIMIT 1
        """,
        (minutes, minutes)
    ).fetchone()
    connection.close()

    if rate is None:
        raise ValueError("No active parking rate matches this duration.")

    return minutes, rate["amount"]

# parking record module

def find_vehicle_record(registration_number):
    """
    Finds the active parking record for a vehicle.

    Only records where exit_time is NULL are considered
    active parking records.
    """

    connection = get_db()

    record = connection.execute(
        """
        SELECT

            pr.record_id,
            pr.entry_time,

            v.vehicle_id,
            v.registration_number,
            v.vehicle_type,

            ps.slot_id,
            ps.slot_number

        FROM parking_records pr

        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id

        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id

        WHERE v.registration_number = ?

        AND pr.exit_time IS NULL

        ORDER BY pr.record_id DESC

        LIMIT 1
        """,
        (registration_number,)
    ).fetchone()

    connection.close()

    return record


# queue module

def promote_waiting_vehicle():
    """
    Queue algorithm

    If a parking slot becomes available and there are
    vehicles waiting, the first vehicle in the queue
    gets the available slot.

    This follows FIFO:

        First vehicle added
                ↓
        First vehicle served
    """

    # Nothing to do if the queue is empty.
    if not waiting_queue:

        return

    # Find an available parking slot.
    slot = find_available_slot()

    if slot is None:

        return

    # Remove the first vehicle from the queue.
    vehicle = waiting_queue.popleft()

    connection = get_db()

    try:

        # Check whether the vehicle is already parked.
        existing = connection.execute(
            """
            SELECT pr.record_id

            FROM parking_records pr

            JOIN vehicles v
                ON pr.vehicle_id = v.vehicle_id

            WHERE v.registration_number = ?

            AND pr.exit_time IS NULL
            """,
            (vehicle["registration_number"],)
        ).fetchone()

        if existing:

            connection.commit()

            return

        # Find the vehicle in the database.
        vehicle_row = connection.execute(
            """
            SELECT vehicle_id
            FROM vehicles
            WHERE registration_number = ?
            """,
            (vehicle["registration_number"],)
        ).fetchone()

        # If the vehicle does not exist, create it.
        if not vehicle_row:

            connection.execute(
                """
                INSERT INTO vehicles
                (registration_number, vehicle_type)
                VALUES (?, ?)
                """,
                (
                    vehicle["registration_number"],
                    vehicle["vehicle_type"]
                )
            )

            vehicle_id = connection.execute(
                "SELECT last_insert_rowid() AS id"
            ).fetchone()["id"]

        else:

            vehicle_id = vehicle_row["vehicle_id"]

        # Get current time.
        now = datetime.now()

        # Mark slot as occupied.
        connection.execute(
            """
            UPDATE parking_slots

            SET status = 'OCCUPIED'

            WHERE slot_id = ?
            """,
            (slot["slot_id"],)
        )

        # Create parking record.
        connection.execute(
            """
            INSERT INTO parking_records
            (
                vehicle_id,
                slot_id,
                entry_time
            )

            VALUES (?, ?, ?)
            """,
            (
                vehicle_id,
                slot["slot_id"],
                now.isoformat(timespec="seconds")
            )
        )

        connection.commit()

        flash(
            f"Waiting vehicle "
            f"{vehicle['registration_number']} "
            f"has been assigned slot "
            f"{slot['slot_number']}.",
            "success"
        )

    finally:

        connection.close()

# dashboard

@app.route("/")
def dashboard():
    """
    Main system dashboard.

    This page displays:

    - Parking availability
    - Active vehicles
    - Completed parking records
    - Waiting queue
    """

    connection = get_db()

    # Get all parking slots.
    slots = connection.execute(
        """
        SELECT *
        FROM parking_slots
        ORDER BY slot_id
        """
    ).fetchall()

    # Get currently parked vehicles.
    active_records = connection.execute(
        """
        SELECT

            pr.record_id,

            v.registration_number,
            v.vehicle_type,

            ps.slot_number,

            pr.entry_time

        FROM parking_records pr

        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id

        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id

        WHERE pr.exit_time IS NULL

        ORDER BY pr.entry_time
        """
    ).fetchall()

    # Get recent completed records.
    completed_records = connection.execute(
        """
        SELECT

            pr.record_id,

            v.registration_number,
            v.vehicle_type,

            ps.slot_number,

            pr.entry_time,
            pr.exit_time,

            pr.duration,
            pr.amount_paid

        FROM parking_records pr

        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id

        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id

        WHERE pr.exit_time IS NOT NULL

        ORDER BY pr.exit_time DESC

        LIMIT 10
        """
    ).fetchall()

    rates = connection.execute(
        """
        SELECT *
        FROM parking_rates
        WHERE active = 1
        ORDER BY minimum_minutes
        """
    ).fetchall()

    connection.close()

    # Count available slots.
    available = sum(
        1
        for slot in slots
        if slot["status"] == "AVAILABLE"
    )

    # Calculate occupied slots.
    occupied = len(slots) - available

    return render_template(
        "index.html",

        slots=slots,

        active_records=active_records,

        completed_records=completed_records,

        available=available,

        occupied=occupied,

        total=len(slots),

        queue=list(waiting_queue),

        rates=rates
    )


@app.route("/api/availability")
def availability_api():
    """Provide the current slot status for the web and entrance displays."""
    slots = get_slots()
    available = sum(1 for slot in slots if slot["status"] == "AVAILABLE")

    return jsonify({
        "available": available,
        "occupied": len(slots) - available,
        "total": len(slots),
        "slots": [
            {"number": slot["slot_number"], "status": slot["status"]}
            for slot in slots
        ]
    })


@app.route("/display")
def entrance_display():
    """A distraction-free display suitable for a screen at the entrance."""
    return render_template("display.html")


@app.route("/rates")
def manage_rates():
    """Show rate bands that management can maintain without editing code."""
    connection = get_db()
    rates = connection.execute(
        "SELECT * FROM parking_rates ORDER BY active DESC, minimum_minutes"
    ).fetchall()
    connection.close()
    return render_template("rates.html", rates=rates)


@app.route("/rates/<int:rate_id>/update", methods=["POST"])
def update_rate(rate_id):
    try:
        minimum = int(request.form.get("minimum_minutes", ""))
        maximum_text = request.form.get("maximum_minutes", "").strip()
        maximum = int(maximum_text) if maximum_text else None
        amount = float(request.form.get("amount", ""))
    except ValueError:
        flash("Rate values must be valid numbers.", "error")
        return redirect(url_for("manage_rates"))

    if minimum < 0 or amount < 0 or (maximum is not None and maximum < minimum):
        flash("Use a valid range and a non-negative amount.", "error")
        return redirect(url_for("manage_rates"))

    connection = get_db()
    connection.execute(
        """
        UPDATE parking_rates
        SET minimum_minutes = ?, maximum_minutes = ?, amount = ?, updated_at = ?
        WHERE rate_id = ?
        """,
        (minimum, maximum, amount, datetime.now().isoformat(timespec="seconds"), rate_id)
    )
    connection.commit()
    connection.close()
    flash("Parking rate updated.", "success")
    return redirect(url_for("manage_rates"))


@app.route("/rates/<int:rate_id>/toggle", methods=["POST"])
def toggle_rate(rate_id):
    connection = get_db()
    connection.execute(
        """
        UPDATE parking_rates
        SET active = CASE active WHEN 1 THEN 0 ELSE 1 END,
            updated_at = ?
        WHERE rate_id = ?
        """,
        (datetime.now().isoformat(timespec="seconds"), rate_id)
    )
    connection.commit()
    connection.close()
    flash("Rate status updated.", "success")
    return redirect(url_for("manage_rates"))

# vehicle entry module

@app.route("/entry", methods=["POST"])
def vehicle_entry():
    """
    Vehicle Entry Module.

    Steps:

    1. Read registration number.
    2. Read vehicle type.
    3. Check whether vehicle is already parked.
    4. Find available parking slot.
    5. Store vehicle.
    6. Mark slot as occupied.
    7. Record entry time.

    If parking is full, vehicle is added to the waiting queue.
    """

    registration = request.form.get(
        "registration_number",
        ""
    ).strip().upper()

    vehicle_type = request.form.get(
        "vehicle_type",
        ""
    ).strip()

    # Validate input.
    if not registration or not vehicle_type:

        flash(
            "Please enter the registration number "
            "and vehicle type.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    # Check whether the vehicle is already parked.
    if find_vehicle_record(registration):

        flash(
            "This vehicle is already parked.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    # Search for an available slot.
    slot = find_available_slot()

    # If there is no available slot...
    if slot is None:

        # Add vehicle to FIFO queue.
        if not any(
            item["registration_number"] == registration
            for item in waiting_queue
        ):

            waiting_queue.append(
                {
                    "registration_number": registration,
                    "vehicle_type": vehicle_type
                }
            )

            flash(
                "Parking is full. "
                "Vehicle added to the waiting queue.",
                "info"
            )

        else:

            flash(
                "Vehicle is already in the waiting queue.",
                "error"
            )

        return redirect(
            url_for("dashboard")
        )

    connection = get_db()

    try:

        # Check whether the vehicle already exists.
        vehicle = connection.execute(
            """
            SELECT vehicle_id

            FROM vehicles

            WHERE registration_number = ?
            """,
            (registration,)
        ).fetchone()

        # If it doesn't exist, insert it.
        if vehicle is None:

            connection.execute(
                """
                INSERT INTO vehicles
                (
                    registration_number,
                    vehicle_type
                )

                VALUES (?, ?)
                """,
                (
                    registration,
                    vehicle_type
                )
            )

            vehicle_id = connection.execute(
                "SELECT last_insert_rowid() AS id"
            ).fetchone()["id"]

        else:

            vehicle_id = vehicle["vehicle_id"]

        # Record current time.
        now = datetime.now()

        # Mark parking slot occupied.
        connection.execute(
            """
            UPDATE parking_slots

            SET status = 'OCCUPIED'

            WHERE slot_id = ?
            """,
            (slot["slot_id"],)
        )

        # Create parking record.
        connection.execute(
            """
            INSERT INTO parking_records
            (
                vehicle_id,
                slot_id,
                entry_time
            )

            VALUES (?, ?, ?)
            """,
            (
                vehicle_id,
                slot["slot_id"],
                now.isoformat(timespec="seconds")
            )
        )

        connection.commit()

        flash(
            f"Vehicle {registration} entered successfully. "
            f"Assigned slot {slot['slot_number']}.",
            "success"
        )

    except sqlite3.IntegrityError:

        connection.rollback()

        flash(
            "The vehicle registration already exists.",
            "error"
        )

    finally:

        connection.close()

    return redirect(
        url_for("dashboard")
    )


# vehicle exit module

@app.route("/exit", methods=["POST"])
def vehicle_exit():
    """
    Vehicle Exit Module.

    Steps:

    1. Receive registration number.
    2. Find parking record.
    3. Record exit time.
    4. Calculate parking duration.
    5. Calculate parking fee.
    6. Check payment.
    7. If payment succeeds:
       - close parking record
       - release slot
       - open barrier
    8. Otherwise:
       - keep barrier closed
    """

    registration = request.form.get(
        "registration_number",
        ""
    ).strip().upper()

    payment_text = request.form.get(
        "payment",
        "0"
    ).strip()

    payment_method = request.form.get("payment_method", "").strip().upper()
    transaction_reference = request.form.get(
        "transaction_reference", ""
    ).strip().upper()

    # Convert payment to a number.
    try:

        payment = float(payment_text)

    except ValueError:

        payment = -1

    if payment_method not in {"MPESA", "CARD", "CASH"}:
        flash("Select M-Pesa, card, or cash as the payment method.", "error")
        return redirect(url_for("dashboard"))

    if payment_method in {"MPESA", "CARD"} and not transaction_reference:
        flash("Enter the M-Pesa or card transaction reference.", "error")
        return redirect(url_for("dashboard"))

    # Find vehicle's active parking record.
    record = find_vehicle_record(
        registration
    )

    # Vehicle doesn't exist.
    if not record:

        flash(
            "Vehicle not found in the parking area. "
            "Barrier remains closed.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    # Convert stored entry time back to datetime.
    try:

        entry_time = datetime.fromisoformat(
            record["entry_time"]
        )

    except ValueError:

        flash(
            "Invalid entry time stored for this vehicle.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    # Current time becomes exit time.
    exit_time = datetime.now()

    # Calculate parking duration and fee.
    try:
        minutes, amount = calculate_fee(entry_time, exit_time)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("dashboard"))

    # Check whether payment is sufficient.
    if payment < amount:

        flash(
            f"Payment insufficient. "
            f"Required: KSh {amount:.2f}. "
            f"Barrier remains closed.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    connection = get_db()

    try:

        change_given = max(0, payment - amount)
        vat_rate = 16
        # The parking charge is treated as VAT-inclusive for this simulation.
        vat_amount = round(amount * vat_rate / (100 + vat_rate), 2)

        # Update the parking record.
        connection.execute(
            """
            UPDATE parking_records

            SET
                exit_time = ?,
                duration = ?,
                amount_paid = ?

            WHERE record_id = ?
            """,
            (
                exit_time.isoformat(
                    timespec="seconds"
                ),
                minutes,
                amount,
                record["record_id"]
            )
        )

        # A payment transaction is retained separately for audit and reports.
        connection.execute(
            """
            INSERT INTO payments
            (
                record_id, amount_due, amount_received, change_given,
                payment_method, transaction_reference, payment_status,
                paid_at, vat_rate, vat_amount
            )
            VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMED', ?, ?, ?)
            """,
            (
                record["record_id"], amount, payment, change_given,
                payment_method,
                transaction_reference if transaction_reference else None,
                exit_time.isoformat(timespec="seconds"),
                vat_rate, vat_amount
            )
        )

        # Release the parking slot.
        connection.execute(
            """
            UPDATE parking_slots

            SET status = 'AVAILABLE'

            WHERE slot_id = ?
            """,
            (record["slot_id"],)
        )

        connection.commit()

    finally:

        connection.close()

    # Simulate opening the barrier.
    flash(
        f"Payment successful. "
        f"KSh {amount:.2f} confirmed by {payment_method}. "
        f"Parking time: {minutes} minute(s). "
        f"Barrier OPEN — vehicle {registration} may exit.",
        "success"
    )

    # Check whether someone is waiting.
    promote_waiting_vehicle()

    return redirect(
        url_for("dashboard")
    )

# reporting module

@app.route("/reports")
def reports():
    """Daily reconciliation and VAT information from immutable payments."""
    selected_date = request.args.get("date", datetime.now().date().isoformat())
    connection = get_db()

    summary = connection.execute(
        """
        SELECT
            COUNT(*) AS transactions,
            COALESCE(SUM(amount_due), 0) AS gross_revenue,
            COALESCE(SUM(vat_amount), 0) AS vat_collected
        FROM payments
        WHERE payment_status = 'CONFIRMED'
          AND DATE(paid_at) = DATE(?)
        """,
        (selected_date,)
    ).fetchone()

    by_method = connection.execute(
        """
        SELECT payment_method, COUNT(*) AS transaction_count,
               COALESCE(SUM(amount_due), 0) AS total_collected
        FROM payments
        WHERE payment_status = 'CONFIRMED'
          AND DATE(paid_at) = DATE(?)
        GROUP BY payment_method
        ORDER BY payment_method
        """,
        (selected_date,)
    ).fetchall()

    transactions = connection.execute(
        """
        SELECT p.*, v.registration_number, ps.slot_number
        FROM payments p
        JOIN parking_records pr ON p.record_id = pr.record_id
        JOIN vehicles v ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps ON pr.slot_id = ps.slot_id
        WHERE DATE(p.paid_at) = DATE(?)
        ORDER BY p.paid_at DESC
        """,
        (selected_date,)
    ).fetchall()
    connection.close()

    return render_template(
        "reports.html",
        selected_date=selected_date,
        summary=summary,
        by_method=by_method,
        transactions=transactions
    )
# Create database and initial parking slots (runs on Render too).
initialize_database()
# start application

if __name__ == "__main__":
    app.run(debug=True)
