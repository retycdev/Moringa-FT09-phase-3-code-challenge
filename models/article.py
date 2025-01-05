from database.connection import get_db_connection
# from models.magazine import Magazine
# from models.author import Author

class Article:
    def __init__(self, title, author_id, magazine_id):
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and (5 <=len(value)<= 50):
            self._title = value
        else:
            raise ValueError("Title must be a string between 5 and 50 characters")
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        from models.author import Author
        if isinstance(value, Author):
            self._author = value
        else: 
            raise ValueError("Author must be an instance of Author")
        
    @property
    def magazine(self):
        return self._magazine
    
    @magazine.setter
    def magazine(self, value):
        from models.magazine import Magazine

        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise ValueError("Magazine must be an instance of Magazine")
        
    def save(self):
        
        

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM authors WHERE name = ?", (self.author.name,))
        author_id = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM magazines WHERE name = ?', (self.magazine.name,))
        magazine_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)', 
                       (self.title, author_id, magazine_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        articles = cursor.fetchall()
        conn.close()
        return articles