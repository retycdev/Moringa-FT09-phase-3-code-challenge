from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine


class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = self.validate_name(name)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Name must be longer than 0 characters")
        return name

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, content, author_id, magazine_id
            FROM articles
            WHERE author_id = ?
            """,
            (self.id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            Article(row["id"], row["title"], row["content"], self, Magazine(row["magazine_id"]))
            for row in rows
        ]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
            """,
            (self.id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS authors")
        conn.commit()
        conn.close()
