import sqlite3


class UserClick():
    def __init__(self, user:str, email:str, datetime:str):
        self.user = user
        self.email = email
        self.datetime = datetime
        
    @classmethod
    def drop_table(cls) -> bool:
        try:
            conn = sqlite3.connect('db.sqlite3')
            conn.execute('DROP TABLE IF EXISTS user_click;')
            conn.commit()
            conn.close()
            
            return True
        
        except Exception:
            return False
        
        
    @classmethod
    def all(cls) -> list[dict]:

        all_items = []
        
        conn = sqlite3.connect('db.sqlite3')
        
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_click;')
        
        all_items = [{
            'user': row[1],
            'email': row[2],
            'datetime': row[3]
            } for row in cur.fetchall()]
        
        conn.close()
        
        return all_items

        
    def save(self) -> bool:
        
        try:
            conn = sqlite3.connect('db.sqlite3')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS user_click
                (id INTEGER PRIMARY KEY,
                user TEXT NOT NULL,
                email TEXT NOT NULL,
                datetime TEXT NOT NULL);''')
            
            conn.execute(f'''
                        INSERT INTO user_click (user, email, datetime) 
                        VALUES ('{self.user}', '{self.email}', '{self.datetime}')
                        ''')
            conn.commit()
            conn.close()
            
            return True
        
        except Exception:
            return False
    
    def to_dict(self) -> dict:
        return {
            'user': self.user,
            'email': self.email,
            'datetime': self.datetime
        }