import os

from hashlib import new
from flask import Flask, request
import json

from db import db, User, Lost, Found

app = Flask(__name__)
db_filename = "lost_and_found.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# Helper methods


def extract_token(request):
    bearer_token = request.headers.get("Authorization")
    if bearer_token is None:
        return False, None
    return True, bearer_token


def success_response(response, code=200):
    return json.dumps(response), code


def failure_response(response, code=404):
    return json.dumps(response), code


db.init_app(app)
with app.app_context():
    db.create_all()

# Routes


@app.route("/")
def home():
    return "Backend server for CUFindIt"


@app.route("/api/register/", methods=["POST"])
def register_account():
    body = json.loads(request.data)
    if body.keys() < {"email", "password"}:
        return failure_response({"error": True}, 400)
    if not User.query.filter_by(email=body["email"]).first() is None:
        return failure_response({"error": True}, 400)
    new_user = User(body["email"], body["password"])
    db.session.add(new_user)
    db.session.commit()
    return success_response({
        "session_token": new_user.session_token,
        "session_expiration": str(new_user.session_expiration),
        "update_token": new_user.update_token,
        "detail": new_user.serialize()
    }, 201)


@app.route("/api/login/", methods=["POST"])
def login():
    body = json.loads(request.data)
    if body.keys() < {"email", "password"}:
        return failure_response({"error": True}, 400)
    user = User.query.filter_by(email=body["email"]).first()
    success = user is not None and user.verify_password(body["password"])
    if not success:
        return failure_response({"error": True}, 401)
    else:
        return success_response({
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
            "detail": user.serialize()
        }, )


@app.route("/api/session/", methods=["POST"])
def update_session():
    success, update_token = extract_token(request)
    if not success:
        return failure_response({"error": True}, 400)
    user = User.query.filter_by(update_token=update_token).first()
    if user is None:
        return failure_response({"error": True}, 400)
    user.renew_session()
    db.session.commit()
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    }, )


@app.route("api/item/<int:item_id>")
def get_found(item_id):
    found = Found.query.filter_by(id=found_id).first()
    if found is None:
        return failure_response({"error": True})
    return success_response(lost.serialize())

def get_claimed(item_id):
    claimed = Claimed.query.filter_by(id=claimed_id).first()
    if claimed is None:
        return failure_response({"error": True})
    return success_response(found.serialize())


@app.route("/api/item/user/")
def get_item_user():
    success, session_token = extract_token(request)
    user = User.query.filter_by(session_token=session_token).first()
    if user is None:
        return failure_response({"error": True})
    success = user.verify_session_token(session_token)
    if not success:
        return failure_response({"error": True}, 401)
    item = item.query.filter_by(user_id=user.id)
    return success_response([l.serialize() for l in item])


@app.route("/api/item/", methods=['POST'])
def post_item():

    success, session_token = extract_token(request)

    user = User.query.filter_by(session_token=session_token).first()
    if user is None:
        return failure_response({"error": True})

    success = user.verify_session_token(session_token)
    if not success:
        return failure_response({"error": True}, 401)

    body = json.loads(request.data)
    if body.keys() < {"name"}:
        return failure_response({"error": True}, 400)

    item = item(
        name=body["name"],
        contact=body.get("contact", None),
        image=body.get("image", None),
        date_found=body.get("date_found", None),
        location=body.get("location", None),
        user_id=user.id,
    )
    db.session.add(item)
    db.session.commit()
    return success_response(item.serialize(), 201)



@app.route("/api/item/<int:item_id>/", methods=["DELETE"])
def delete_item(item_id):

    success, session_token = extract_token(request)

    user = User.query.filter_by(session_token=session_token).first()
    if user is None:
        return failure_response({"error": True})

    success = user.verify_session_token(session_token)

    if not success:
        return failure_response({"error": True}, 401)
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response({"error": True})
    db.session.delete(item)
    db.session.commit()
    return success_response(item.serialize())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)