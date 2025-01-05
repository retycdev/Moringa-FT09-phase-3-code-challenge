from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category=None):
        """
        Initialize a Magazine instance.

        :param id: Unique identifier for the magazine.
        :param name: Name of the magazine.
        :param category: Category of the magazine (optional).
        """
        self._id = id
        self.name = name
        self.category = category if category else "Uncategorized"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
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
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (self.name, self.category),
        )
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (self.id,),
        )
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ?
            """,
            (self.id,),
        )
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def articles_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title FROM articles WHERE magazine_id = ?",
            (self.id,),
        )
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT authors.id, authors.name 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ? 
            GROUP BY authors.id 
            HAVING COUNT(*) > 2
            """,
            (self.id,),
        )
        authors = cursor.fetchall()
        conn.close()
        return authors
