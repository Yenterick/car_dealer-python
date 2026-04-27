"""
Seed data script — populates every table with sample rows.
Run from the project root:  python -m db.seed_data
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "car_dealer.db")


def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # ── Suppliers ──────────────────────────────────────────────
    suppliers = [
        ("AutoParts Global", "contacto@autopartsglobal.com", "+57 301 234 5678"),
        ("Toyota Colombia", "ventas@toyotacol.com", "+57 310 876 5432"),
        ("Chevrolet Distributor", "info@chevydist.com", "+57 315 111 2233"),
        ("Hyundai Motors", "soporte@hyundaimotors.co", "+57 320 444 5566"),
        ("Repuestos Express", "ventas@repuestosexpress.com", "+57 318 777 8899"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO supplier (name, email, phone) VALUES (?, ?, ?)",
        suppliers,
    )

    # ── Cars ───────────────────────────────────────────────────
    cars = [
        ("Corolla", 2024, "Sedan", 2),
        ("Hilux", 2023, "Truck", 2),
        ("Onix", 2024, "Sedan", 3),
        ("Tracker", 2023, "SUV", 3),
        ("Tucson", 2024, "SUV", 4),
        ("Accent", 2022, "Sedan", 4),
        ("Fortuner", 2024, "SUV", 2),
        ("Camaro", 2023, "Coupe", 3),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO car (model, year, type, supplier_id) VALUES (?, ?, ?, ?)",
        cars,
    )

    # ── Spares ─────────────────────────────────────────────────
    spares = [
        ("Filtro de Aceite", "Motor", 1),
        ("Pastillas de Freno", "Frenos", 1),
        ("Amortiguador Delantero", "Suspensión", 5),
        ("Batería 12V", "Eléctrico", 5),
        ("Correa de Distribución", "Motor", 2),
        ("Radiador", "Refrigeración", 3),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO spare (name, type, supplier_id) VALUES (?, ?, ?)",
        spares,
    )

    # ── Customers ──────────────────────────────────────────────
    customers = [
        ("1023456789", "Carlos", "Martínez"),
        ("1098765432", "María", "López"),
        ("1012345678", "Andrés", "García"),
        ("1087654321", "Laura", "Rodríguez"),
        ("1056789012", "Santiago", "Hernández"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO customer (dni, name, last_name) VALUES (?, ?, ?)",
        customers,
    )

    # ── Employees ──────────────────────────────────────────────
    employees = [
        ("8001234567", "Pedro", "Ramírez"),
        ("8009876543", "Ana", "Torres"),
        ("8005678901", "Luis", "Morales"),
        ("8004321098", "Camila", "Vargas"),
        ("8007890123", "Diego", "Castillo"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO employee (dni, name, last_name) VALUES (?, ?, ?)",
        employees,
    )

    # ── Buys (purchases from suppliers) ────────────────────────
    buys = [
        (85000000, 2, 1, None),    # Compra Corolla a Toyota
        (120000000, 2, 7, None),   # Compra Fortuner a Toyota
        (45000, 1, None, 1),       # Compra Filtro de Aceite a AutoParts
        (320000, 5, None, 3),      # Compra Amortiguador a Repuestos Express
        (95000000, 3, 8, None),    # Compra Camaro a Chevrolet
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO buy (cost, supplier_id, car_id, spare_id) VALUES (?, ?, ?, ?)",
        buys,
    )

    # ── Sales ──────────────────────────────────────────────────
    sales = [
        (95000000, 1, 1, 1, None),    # Venta Corolla a Carlos por Pedro
        (135000000, 2, 2, 7, None),   # Venta Fortuner a María por Ana
        (60000, 3, 3, None, 1),       # Venta Filtro de Aceite a Andrés por Luis
        (110000000, 4, 4, 5, None),   # Venta Tucson a Laura por Camila
        (450000, 5, 5, None, 3),      # Venta Amortiguador a Santiago por Diego
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO sale (value, customer_id, employee_id, car_id, spare_id) VALUES (?, ?, ?, ?, ?)",
        sales,
    )

    conn.commit()
    print(f"[OK] Seed data inserted successfully into {DB_PATH}")

    # Quick verification
    for table in ["supplier", "car", "spare", "customer", "employee", "buy", "sale"]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"   {table}: {count} rows")

    conn.close()


if __name__ == "__main__":
    seed()
