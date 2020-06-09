import sqlite3

class Setup:
    def run():
        conn = sqlite3.connect('republicabeerbot.db')

        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS schedules
                     (id integer PRIMARY KEY, time varchar(10) NOT NULL, duration int NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        conn.commit()

        conn.close()
