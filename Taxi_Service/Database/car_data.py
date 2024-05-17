import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('car_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table named 'car_info' with the specified columns
cursor.execute('''CREATE TABLE IF NOT EXISTS car_info
              (id INTEGER PRIMARY KEY, car_model TEXT, driver_name TEXT, country_region TEXT, rating TEXT)''')

# Insert example data into the table
example_data = [
    ('Toyota Camry', 'Alice', 'Baku', '4/5'),
    ('Honda Civic', 'Bob', 'Lenkeran', '3/5'),
    ('Ford Mustang', 'Charlie', 'Masalli', '5/5'),
    ('Tesla Model S', 'David', 'Quba', '4/5'),
    ('BMW 3 Series', 'Eve', 'Gabala', '5/5')
]

cursor.executemany('INSERT INTO car_info (car_model, driver_name, country_region, rating) VALUES (?, ?, ?, ?)', example_data)

# Commit changes to the database
conn.commit()

# Close the connection
conn.close()
