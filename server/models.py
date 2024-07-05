from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validates_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Failed name validation")

        existing_author = Author.query.filter(Author.name == name).first()

        if existing_author and (not self.id or existing_author.id != self.id):
            raise ValueError("Name must be unique among authors")

        return name

    @validates('phone_number')
    def validates_phone(self, key, number):
        if number and (len(number) != 10 or not number.isdigit()):
            raise ValueError("Failed number validation")

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validates_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Failed content length validation")

    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Failed summary length validation")

    @validates('category')
    def validates_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Failed category type validation")

    @validates('title')
    def validates_title(self, key, title):
        title_keys = ["Won't Believe", "Secret", "Top", "Guess" ]

        for key in title_keys:
            if key in title:
                return title

        raise ValueError("Failed title validation")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
