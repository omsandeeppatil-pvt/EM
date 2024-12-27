import sqlite3

def init_db():
    """Initialize the SQLite database and create the employees table if it doesn't exist."""
    try:
        # Connect to SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()

        # Create the employees table
        c.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                joining_date TEXT NOT NULL,
                status TEXT DEFAULT 'Active'
            )
        ''')
        conn.commit()
        print("Database initialized successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        # Ensure the connection is always closed
        conn.close()

if __name__ == '__main__':
    init_db()
