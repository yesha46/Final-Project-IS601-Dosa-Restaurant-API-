import sqlite3
import json

# Connect to the database

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Load JSON data

with open("example_orders.json") as file:
    orders_data = json.load(file)

for entry in orders_data:
    name = entry["name"]
    phone = entry["phone"]
    items = entry["items"]

    # Insert or find the customer

    cursor.execute("SELECT id FROM customers WHERE name = ? AND email = ?", (name, phone))
    result = cursor.fetchone()
    if result:
        customer_id = result[0]
    else:
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, phone))
        customer_id = cursor.lastrowid

    # Insert each item and corresponding order

    for item in items:
        item_name = item["name"]
        price = item["price"]

        # Insert or find the item

        cursor.execute("SELECT id FROM items WHERE name = ? AND price = ?", (item_name, price))
        result = cursor.fetchone()

        if result:
            item_id = result[0]
        else:
            cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item_name, price))
            item_id = cursor.lastrowid

        # Insert order

        cursor.execute("INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?)", (customer_id, item_id, 1))

conn.commit()
conn.close()

print("Data loaded successfully.")