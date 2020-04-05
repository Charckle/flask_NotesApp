# Import the database object (db) from the main application module

from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'users_table'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)
    
    # UserName
    username    = db.Column(db.String(128),  nullable=False,
                            unique=True)    

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                         unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, username, email, password):

        self.name     = username
        self.username = username
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)        