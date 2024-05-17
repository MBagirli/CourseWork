import sqlite3
import hashlib

def create_users_table():
    connection = sqlite3.connect('credentials.db')
    cursor = connection.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    '''

    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

def add_user(username, password):
    connection = sqlite3.connect('credentials.db')
    cursor = connection.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    insert_user_query = '''
        INSERT INTO users (username, password_hash) VALUES (?, ?);
    '''

    cursor.execute(insert_user_query, (username, password_hash))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_users_table()
    add_user('admin', 'admin')
