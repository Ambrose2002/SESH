import json
from db import db
from db import Users, Seshs
from flask import Flask, request
import users_dao

app = Flask(__name__)
db_filename = "sessions.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    """
    Generalized success response function
    """
    return json.dumps(data), code

def failure_response(message, code=404):
    """
    Generalized failure response function
    """
    return json.dumps({"error": message}), code

def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_token = request.headers.get("Authorization")
    if auth_token is None:
        return False, failure_response("Missing authorization")
    
    bearer_token = auth_token.replace("Bearer", "").strip()
    if not bearer_token:
        return False, failure_response("Invalid Authorization header")
    return True, bearer_token

@app.route("/")

@app.route("/api/users/")
def get_users():
    """Returns a json of all users"""
    users = [user.serialize() for user in Users.query.all()]
    return success_response(users, 200)

# @app.route("/api/users/", methods= ["POST"])
# def create_user():
#     body = json.loads(request.data)
#     netid = body.get("netid")
#     if netid is None:
#         return json.dumps({"error":"Provide netid"}), 400
#     email = body.get("email")
#     if email is None:
#         return failure_response("Provide email")
#     password= body.get("password")
#     if password is None:
#         return json.dumps({"error":"Provide password"}), 400

#     user = Users(
#         netid = body.get("netid"),
#         email = body.get("email"), 
#         password = body.get("password")
#     )
#     db.session.add(user)
#     db.session.commit()
#     return json.dumps(user.simple_serialize()), 400

@app.route("/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)
    first_name = body.get("first_name")
    email = body.get("email")
    password = body.get("password")
    
    if first_name is None or email is None or password is None:
        return failure_response("Invalid body")
    created, user = users_dao.create_user(first_name, email, password)
    
    if not created:
        return failure_response("User already exists")
    return success_response({"session_token": user.session_token,
                       "session_expiration": str(user.session_expiration),
                       "update_token": user.update_token})


@app.route("/api/sessions/")
def get_sessions():
    """
    Endpoint for getting all study sessions
    """
    sessions = []
    for sesh in Seshs.query.all():
        sessions.append(sesh.serialize())
    return json.dumps({"sessions": sessions}), 200

@app.route("/api/sessions/<int:user_id>/", methods = ["POST"])
def create_session(user_id):
    """
    endpoint for adding a session
    """
    user = Users.query.filter_by(id = user_id).first()
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    body = json.loads(request.data)
    title = body.get("title")
    course = body.get("course")
    date = body.get("date") 
    start_time = body.get("start_time") 
    end_time = body.get("end_time") 
    location = body.get("location") 
    description = body.get("description")

    args = [title, course, date, start_time, end_time, location]

    if not all(arg is not None for arg in args):
        return json.dumps({"error": "Illegal arguments!"}), 400
    new_session = Seshs(
      title = title,
      course = course,
      date = date, 
      admin = user_id,
      start_time = start_time,
      end_time = end_time,
      location = location, 
      description = description
    )
    user.seshs.append(new_session)
    db.session.add(new_session)
    new_session.population += 1
    db.session.commit()
    return json.dumps(new_session.simple_serialize()), 201

@app.route("/api/sessions/<int:session_id>/<int:user_id>/", methods = ["DELETE"])
def delete_session(session_id, user_id):
    """
    Endpoint for deleting a session from a users sessions
    """
    session = Seshs.query.filter_by(id=session_id).first()
    user = Users.query.filter_by(id=user_id).first()
    if session is None or user is None:
        return json.dumps({"error": "Session or User not found!"}), 404
    user.seshs.remove(session)
    db.session.commit()
    return json.dumps(session.simple_serialize()), 200


@app.route("/api/sessions/<int:user_id>/", methods = ["GET"])
def get_user_sesh(user_id):
    """Endpont for getting all the sessions attributed to a user"""
    user = Users.query.filter_by(id = user_id).first()
    sessions = []
    for sesh in user.seshs:
        sessions.append(sesh.simple_serialize())
    return json.dumps(sessions)
    

@app.route("/api/sessions/filter/", methods = ["GET"])
def get_by_filter():
    """Endpoint for querying sessions by title, course and date"""
    body = json.loads(request.data)
    for param in body:
        if param == "title":
            title = body.get("title")
            sessions = Seshs.query.filter(Seshs.title.like(f"%{title}%"))
        elif param == "course":
            course = body.get("course")
            sessions = Seshs.query.filter(Seshs.course.like(f"%{course}%"))
        elif param == "date":
            date = body.get("date")
            sessions = Seshs.query.filter(Seshs.date.like(f"%{date}%"))
        elif param == "location":
            location = body.get("location")
            sessions = Seshs.query.filter(Seshs.location.like(f"%{location}%"))
        else:
            return json.dumps({"error": "Session not found"}), 404
    sessions = [session.simple_serialize() for session in sessions]
    return json.dumps(sessions), 200

@app.route("/api/sessions/<int:session_id>/<int:user_id>/", methods = ["POST"])
def join_session(session_id, user_id):
    """
    Endpoint for adding a user to a session
    """
    session = Seshs.query.filter_by(id=session_id).first()
    user = Users.query.filter_by(id=user_id).first()
    if session is None or user is None:
        return json.dumps({"error": "Session or User not found!"}), 404
    if session not in user.seshs:
        session.population += 1
        user.seshs.append(session)
        db.session.commit()
        return json.dumps(session.simple_serialize()), 200
    return json.dumps({"error": "User already in session!"})


#Authentication
#Deployment




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)