class Article:
    def __init__(self, id, title, content, author, magazine):
        self._id = id
        self.title = title
        self.content = content
        self.author = author
        self.magazine = magazine

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Title must be a non-empty string")
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Content must be a non-empty string")
        self._content = value
