import json
from db import db
from db import Users, Seshs
from flask import Flask, request

app = Flask(__name__)
db_filename = "sessions.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")

@app.route("/api/users/")
def get_users():
    """Returns a json of all users"""
    users = [user.serialize() for user in Users.query.all()]
    return json.dumps(users)

@app.route("/api/users/", methods= ["POST"])
def create_user():
    body = json.loads(request.data)
    netid = body.get("netid")
    if netid is None:
        return json.dumps({"error":"Provide netid"}), 400
    email = body.get("email")
    if email is None:
        return json.dumps({"error":"Provide email"}), 400
    password= body.get("password")
    if password is None:
        return json.dumps({"error":"Provide password"}), 400

    user = Users(
        netid = body.get("netid"),
        email = body.get("email"), 
        password = body.get("password")
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps(user.simple_serialize()), 400


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
    db.users.commit()
    return json.dumps(session.simple_serialize()), 200


@app.route("/api/sessions/<int:user_id>", methods = ["GET"])
def get_user_sesh(user_id):
    pass


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
            print(location)
            sessions = Seshs.query.filter(Seshs.location.like(f"%{location}%"))
            print(sessions)
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
    user.seshs.append(session)
    db.users.commit()
    return json.dumps(session.simple_serialize()), 200


#Authentication
#Deployment




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)