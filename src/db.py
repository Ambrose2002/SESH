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
    netid = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    seshs = db.relationship("Seshs", secondary = assoc_table, back_populates = "users")
    admins = db.relationship("Seshs", cascade = "delete")
    
    
    def __init__(self, **kwargs):
        """Initializes a new user object"""
        self.netid = kwargs.get("netid")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        
        
    def serialize(self):
        """Returns a serialized users object"""
        return {
            "id": self.id,
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
    population = db.Column(db.Integer, autoincrement = True)
    
    
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
        self.population = 1
        
    
    
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
            "population": self.population,
            "description": self.description,
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
    
