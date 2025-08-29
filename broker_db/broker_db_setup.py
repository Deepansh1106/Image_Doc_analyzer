# broker_db_setup.py
import sqlite3
import pandas as pd

def create_broker_db(excel_path='Registered_stock_brokers_in_equity.xlsx', db_path='broker_db.sqlite'):
    # Load Excel
    df = pd.read_excel(excel_path)
    # Expecting first column: Name, second: Registration No.
    df = df.iloc[:, :2]  # just first two columns
    df.columns = ['name', 'registration_no']

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS brokers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            registration_no TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert data
    for _, row in df.iterrows():
        try:
            c.execute('INSERT OR IGNORE INTO brokers (name, registration_no) VALUES (?, ?)',
                      (row['name'], row['registration_no']))
        except Exception as e:
            print(f"Error inserting {row}: {e}")

    conn.commit()
    conn.close()
    print("Broker database created successfully!")

# Quick test
if __name__ == "__main__":
    create_broker_db()
