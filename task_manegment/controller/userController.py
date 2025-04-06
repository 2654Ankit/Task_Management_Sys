from Models.User import Users
from flask import request,make_response,jsonify
from Models.Task import TaskManagger
from Models.TaskLogger import TaskLogger,AuditLog
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from functools import wraps
from sqlalchemy.sql import func
import json
from datetime import datetime,timedelta,timezone
import redis
from Models.TaskLogger import TaskLogger,AuditLog
from datetime import datetime
from extensions import db,get_redis,create_app







def signup():
    data = request.json
    username = data.get("username")
    pas = data.get("password")
    print(pas)
    role = data.get("role")

    if username and pas and role:
        user=Users.query.filter_by(username=username).first()
        if user:
            return make_response(
                {"message":"Please sign in"},
                200
            )
        
        

        user = Users(
            username=username,
            password=generate_password_hash(pas),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return make_response(
            {"message":"user created"},
            201
        )
    return make_response(
        {"message":"User not created"},
        500
    )

def login():
    auth= request.json

    if not auth or not auth.get("username") or not auth.get("password"):
        return make_response(
            "Proper Credentials not provided",
            401

        )
    user = Users.query.filter_by(username=auth.get("username")).first()

    if not user:
        return make_response(
            "please create an account",
            401
        )
    if check_password_hash(user.password,auth.get('password')):
        token = jwt.encode({
            'username':user.username,
            'exp':datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        "secret",
        "HS256"
        )

        return make_response({"token":token})
    return make_response(
        'Please check your credintials',
        401
    )


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            print(token)
        if not token:
            return make_response({"message":"token is missing"})
        
        try:
            data = jwt.decode(token,"secret",algorithms=["HS256"])
            current_user = Users.query.filter_by(username=data["username"]).first()

            print(current_user)

        except Exception as e:
            print(e)
            return make_response({"message":"Token is invalid"},
            401)

        return f(current_user,*args,**kwargs)

    return decorated
