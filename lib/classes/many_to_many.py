class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = title

        self.author = author  
        self.magazine = magazine

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("Author must be an instance of Author")
        if self not in value.articles():
            value._articles.append(self)
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be an instance of Magazine")
        if self not in value.articles():
            value._articles.append(self)
        self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    def articles(self):
        return self._articles.copy()

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self._articles:
            return None
        return list(set(magazine.category for magazine in self.magazines()))


class Magazine:
    _all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")

        self._name = name
        self._category = category
        self._articles = []
        Magazine._all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        return self._articles.copy()

    def contributors(self):
        return list(set(article.author for article in self._articles)) if self._articles else None

    def article_titles(self):
        return [article.title for article in self._articles] if self._articles else None

    def contributing_authors(self):
        author_counts = {}
        for article in self._articles:
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        contributing = [author for author, count in author_counts.items() if count > 2]
        return contributing if contributing else None

    @classmethod
    def top_publisher(cls):
        if not cls._all:
            return None

        max_articles = max(len(mag.articles()) for mag in cls._all)
        top_magazines = [mag for mag in cls._all if len(mag.articles()) == max_articles]
        return top_magazines[0] if top_magazines else None
    
    def __str__(self):
        return f"Magazine(name='{self.name}', category='{self.category}')"
    
    def __repr__(self):
        return self.__str__()