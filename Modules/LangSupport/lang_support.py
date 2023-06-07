import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, language TEXT)')
        self.conn.commit()

    def get_language(self, user_id):
        self.cursor.execute('SELECT language FROM users WHERE id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'en'  # Idioma predeterminado
        else:
            return result[0]

    def set_language(self, user_id, language):
        self.cursor.execute('INSERT OR IGNORE INTO users (id, language) VALUES (?, ?)', (user_id, language))
        self.cursor.execute('UPDATE users SET language = ? WHERE id = ?', (language, user_id))
        self.conn.commit()

    def clear_db(self):
        self.cursor.execute('DELETE from users')
        self.conn.commit()