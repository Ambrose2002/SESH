import datetime
import hashlib
import os

import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

assoc_table = db.Table("assoc", db.Model.metadata,
                       db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                       db.Column("sesh_id", db.Integer, db.ForeignKey("seshs.id"))
                       )

class Users(db.Model):
    """A class for creating Users table
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    seshs = db.relationship("Seshs", secondary = assoc_table, back_populates = "users")
    admins = db.relationship("Seshs", cascade = "delete")
    
    # User information
    netid = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False, unique = False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)
    
    
    def __init__(self, **kwargs):
        """Initializes a new user object"""
        self.first_name = kwargs.get("first_name")
        self.email = kwargs.get("email")
        self.netid = kwargs.get("netid")
        self.email = kwargs.get("email")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()
        
        
    def serialize(self):
        """Returns a serialized users object"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "netid": self.netid,
            "email": self.email,
            "seshs": [sesh.simple_serialize() for sesh in self.seshs]        
        }
    
        
    def simple_serialize(self):
        """Returns a serialized users object without seshs"""
        return{
            "id": self.id,
            "netid": self.netid,
            "email": self.email
        }
    
    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == self.update_token

           
class Seshs(db.Model):
    """A class for creating Seshs table
    """
    __tablename__ = "seshs"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    course = db.Column(db.String, nullable = False)
    date = db.Column(db.String, nullable = False)
    start_time = db.Column(db.String, nullable = False)
    end_time = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    users = db.relationship("Users", secondary = assoc_table, back_populates = "seshs")
    admin = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False) # represents creator of the sesh
    population = db.Column(db.Integer)
    
    
    def __init__(self, **kwargs):
        """Initializes a new user object"""
        self.title = kwargs.get("title")
        self.admin = kwargs.get("admin")  # must be set to user_id in constructor
        self.course = kwargs.get("course")
        self.date = kwargs.get("date")
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")
        self.location = kwargs.get("location")
        self.description = kwargs.get("description", "")
        self.population = 0
       
    
    
    def serialize(self):
        """Returns a serialized sesh object"""
        return {
            "id": self.id,
            "title": self.title,
            "course": self.course,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "description": self.description,
            "population": self.population,
            "users": [user.simple_serialize() for user in self.users]
        }
        
        
    def simple_serialize(self):
        """Returns a serialized sesh object without users"""
        return {
            "id": self.id,
            "title": self.title,
            "course": self.course,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "population": self.population,
            "description": self.description,
        }
    
