from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('All authors must have a name.')
        if self.query.filter_by(name=name).first():
            raise ValueError('No two authors can have the same name.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError('Author phone numbers must be exactly ten digits.')
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('All posts must have a title.')
        if not any(substring in title for substring in ['Won\'t Believe', 'Secret', 'Top', 'Guess']):
            raise ValueError('Post title must be sufficiently clickbait-y.')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Post summary must be a maximum of 250 characters.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Post category must be either "Fiction" or "Non-Fiction".')
        return category
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
