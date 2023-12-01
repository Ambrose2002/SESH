import json
from db import db
from db import Users, Seshs
from flask import Flask, request
import users_dao
import datetime


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


@app.route("/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)
    first_name = body.get("first_name")
    netid = body.get("netid")
    email = body.get("email")
    password = body.get("password")
    
    if first_name is None or email is None or password is None:
        return failure_response("Invalid body")
    created, user = users_dao.create_user(first_name, netid, email, password)
    
    if not created:
        return failure_response("User already exists")
    return success_response({"first_name": first_name,
                             "netid": netid,
                             "email": email,
                             "session_token": user.session_token,
                             "session_expiration": str(user.session_expiration),
                             "update_token": user.update_token})


@app.route("/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    first_name = body.get("first_name")
    email = body.get("email")
    password = body.get("password")
    
    if email is None or password is None:
        return failure_response("Invalid body")
    
    success, user = users_dao.verify_credentials(email, password)
    if not success:
        return failure_response("invalid credentials")
    user.renew_session()
    db.session.commit()
    return json.dumps({"session_token": user.session_token,
                       "session_expiration": str(user.session_expiration),
                       "update_token": user.update_token})
    
    
@app.route("/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    """
    success, response = extract_token(request)
    if not success:
        return response
    update_token = response
    try:
        user = users_dao.renew_session(update_token)
    except Exception as e:
        return failure_response("Invalid update token")
    return json.dumps({
                       "session_token": user.session_token,
                       "session_expiration": str(user.session_expiration),
                       "update_token": user.update_token
    })
    
@app.route("/secret/", methods=["GET"])
def secret_message():
    """
    Endpoint for verifying a session token and returning a secret message

    In your project, you will use the same logic for any endpoint that needs 
    authentication
    """
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")
    return success_response("Hello " + user.first_name)

@app.route("/logout/", methods=["POST"])
def logout():
    """
    Endpoint for logging out a user
    """
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")
    user.session_expiration = datetime.datetime.now()
    db.session.commit()
    return failure_response("You have been logged out")


@app.route("/api/sessions/")
def get_sessions():
    """
    Endpoint for getting all study sessions
    """
    seshs = [sesh.serialize() for sesh in Seshs.query.all()]
    return success_response(seshs, 200)


@app.route("/api/sessions/", methods = ["POST"])
def create_session():
    """
    endpoint for adding a session
    """
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")
    body = json.loads(request.data)
    title = body.get("title")
    course = body.get("course")
    start_time = body.get("start_time") 
    end_time = body.get("end_time") 
    location = body.get("location") 
    description = body.get("description")

    args = [title, course, start_time, end_time, location]

    if not all(arg is not None for arg in args):
        return failure_response("Illegal arguments!", 400)
    new_session = Seshs(
      title = title,
      course = course,
      admin = user.id,
      start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'),
      end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'),
      location = location, 
      description = description
    )
    user.seshs.append(new_session)
    db.session.add(new_session)
    new_session.population += 1
    db.session.commit()
    return success_response(new_session.simple_serialize(), 201)


@app.route("/api/sessions/<int:session_id>/", methods = ["DELETE"])
def delete_session(session_id):
    """
    Endpoint for deleting a session from a users sessions
    """
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")
    session = Seshs.query.filter_by(id=session_id).first()
    if session is None or user is None:
        return failure_response("Session or User not found!", 404)
    try:
        user.seshs.remove(session)
    except Exception as e:
        return failure_response("User not in session")
    session.population-= 1
    db.session.commit()
    return success_response(session.simple_serialize(), 200)


@app.route("/api/sessions/user/", methods = ["GET"])
def get_user_sesh():
    """Endpont for getting all the sessions attributed to a user"""
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")
    sessions = []
    for sesh in user.seshs:
        sessions.append(sesh.simple_serialize())
    return success_response(sessions)
    

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
        elif param == "location":
            location = body.get("location")
            sessions = Seshs.query.filter(Seshs.location.like(f"%{location}%"))
        else:
            return failure_response("Session not found", 404)
    sessions = [session.simple_serialize() for session in sessions]
    return success_response(sessions, 200)


@app.route("/api/sessions/<int:session_id>/", methods = ["POST"])
def join_session(session_id):
    """
    Endpoint for adding a user to a session
    """
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    session = Seshs.query.filter_by(id=session_id).first()
    if session is None or user is None:
        return failure_response("Session or User not found!", 400)
    if session not in user.seshs:
        session.population += 1
        user.seshs.append(session)
        db.session.commit()
        return success_response(session.simple_serialize(), 200)
    return failure_response("User already in session!")

#Deployment


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)