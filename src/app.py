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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)