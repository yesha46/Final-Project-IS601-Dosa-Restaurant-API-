from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Dosa Restaurant API")

# ----------- Customer Schema -----------
class Customer(BaseModel):
    name: str
    phone: str

# ----------- Create Customer -----------
@app.post("/customers/")
def create_customer(customer: Customer):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)",
                       (customer.name, customer.phone))
        conn.commit()
        return {"message": "Customer created successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Phone already exists")
    finally:
        conn.close()

# ----------- Get Customer by ID -----------
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "phone": row[2]}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

# ----------- Update Customer -----------
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, email = ? WHERE id = ?",
                   (customer.name, customer.phone, customer_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")
    conn.close()
    return {"message": "Customer updated successfully"}

# ----------- Delete Customer -----------
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")
    conn.close()
    return {"message": "Customer deleted successfully"}

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", 
                   (item.name, item.price))
    conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "price": row[2]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", 
                   (item.name, item.price, item_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    conn.close()
    return {"message": "Item updated successfully"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    conn.close()
    return {"message": "Item deleted successfully"}

class Order(BaseModel):
    customer_id: int
    item_id: int
    quantity: int

@app.post("/orders/")
def create_order(order: Order):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    # Ensure referenced customer and item exist
    cursor.execute("SELECT id FROM customers WHERE id = ?", (order.customer_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    cursor.execute("SELECT id FROM items WHERE id = ?", (order.item_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Item not found")

    cursor.execute("INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?)",
                   (order.customer_id, order.item_id, order.quantity))
    conn.commit()
    conn.close()
    return {"message": "Order created successfully"}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT orders.id, customers.name, items.name, orders.quantity
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
    JOIN items ON orders.item_id = items.id
    WHERE orders.id = ?
    """, (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "customer_name": row[1], "item_name": row[2], "quantity": row[3]}
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET customer_id = ?, item_id = ?, quantity = ? WHERE id = ?",
                   (order.customer_id, order.item_id, order.quantity, order_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    conn.close()
    return {"message": "Order updated successfully"}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    if cursor.rowcount == 0:    
        raise HTTPException(status_code=404, detail="Order not found")
    conn.close()
    return {"message": "Order deleted successfully"}