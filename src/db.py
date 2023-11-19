from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

assoc_table = db.Table("assoc", db.Model.metadata,
                       db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                       db.Column("sesh_id", db.Integer, db.ForeignKey("sesh.id"))
                       )

class Users(db.Model):
    """A class for creating Users table
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    netid = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    sesh = db.relationship("Seshs", secondary = assoc_table, back_populates = "users")
    
    
    def __init__(self, *kwargs):
        """Initializes a new user object
        """
        self.netid = kwargs.get("netid")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        
        
    def serialize(self):
        """Returns a serialized users object"""
        
        
    
    
class Seshs:
    """A class for creating Seshs table
    """
    __tablename__ = "seshs"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    course = db.Column(db.String, nullable = False)
    date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    location = db.Column(db.String, nullable = False)
    number_of_students = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable = False)
    user = db.relationship("Users", secondary = assoc_table, back_populates = "seshs")
    
    
    def __init__(self, *kwargs):
        """Initializes a new user object
        """
        self.title = kwargs.get("title")
        self.course = kwargs.get("course")
        self.date = kwargs.get("date")
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")
        self.location = kwargs.get("location")
        self.number_of_students = kwargs.get("number_of_students")
        self.description = kwargs.get("description", "")
    
    
    def serialize(self):
        """Returns a serialized sesh object"""
    
