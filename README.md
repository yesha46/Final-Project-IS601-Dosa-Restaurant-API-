Dosa Restaurant Management API

This is a RESTful API backend for managing a Dosa Restaurant, built using FastAPI and SQLite. The API supports full CRUD operations for managing Customers, Items and Orders. It also loads real order data from example_orders.json file.

Project Structure:

dosa_api_project contains the following files:

1. db.sqlite                SQLite database file
2. init_db.py               Initializes the database with required tables
3. main.py                  FastAPI app with all CRUD endpoints
4. load_from_json.py        Loads data from example_orders.json into the database
5. example_orders.json      JSON dataset used to populate customers, items, and orders
6. README.md                


How to Run the Project:

1. Install Dependencies

- Make sure you have Python 3.7+ and install the required packages.
- Run on terminal: pip install fastapi uvicorn

2. Initialize the Database

- Run on terminal: python init_db.py
- This will create db.sqlite with the necessary tables (customers, items, and orders).

3. Load Sample Data from JSON

- Run on terminal: python load_from_json.py
- This will insert real-world order data into the database.

4. Start the FastAPI Server

- Run on terminal: uvicorn main:app --reload
- Open your browser and navigate to http://127.0.0.1:8000/docs
- This opens the interactive Swagger UI for testing all endpoints.

API Endpoints:

1. Customers
- POST /customers/ – Add a new customer
- GET /customers/{id} – Retrieve a customer by ID
- PUT /customers/{id} – Update a customer's information
- DELETE /customers/{id} – Delete a customer

2.Items
- POST /items/ – Add a new menu item
- GET /items/{id} – Get item details
- PUT /items/{id} – Update item info
- DELETE /items/{id} – Delete item

3. Orders
- POST /orders/ – Create a new order (links customer & item)
- GET /orders/{id} – Retrieve order info
- PUT /orders/{id} – Update an order
- DELETE /orders/{id} – Cancel an order

Features:

- FastAPI with auto-generated Swagger UI
- SQLite backend with relational schema and foreign keys
- Data loading from realistic JSON structure
- Modular Python code with clean structure
