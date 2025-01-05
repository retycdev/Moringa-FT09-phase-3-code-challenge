from database.connection import get_db_connection

class Magazine:

    def __init__(self, id, name, category):
        self._id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @property
    def name (self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?,?)", (self.name, self.category))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles
    
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT authors.* FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id=?", (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors
    
    def articles_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id=?",(self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles
    
    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT authors.id, authors.name FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id=? GROUP BY authors.id HAVING COUNT(*) > 2", (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors




    def save(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?,?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        conn.commit()

        self.id = CURSOR.latrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine
    
    def get_magazine_id(self):
        return self.id

        
