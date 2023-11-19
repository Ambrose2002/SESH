import json
from db import db
from db import Users, Seshs
from flask import Flask, request

app = Flask(__name__)
db_filename = "cms.db"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)