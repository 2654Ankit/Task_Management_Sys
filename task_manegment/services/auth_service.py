from repository.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response
import jwt
from datetime import datetime, timedelta, timezone

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def signup(self, data):
        user = self.repo.get_by_username(data["username"])
        if user:
            return make_response({"message": "User already exists"}, 200)

        hashed_pw = generate_password_hash(data["password"])
        self.repo.add_user(data["username"], hashed_pw, data["role"])
        return make_response({"message": "User created"}, 201)

    def login(self, data):
        user = self.repo.get_by_username(data["username"])
        if not user or not check_password_hash(user.password, data["password"]):
            return make_response({"message": "Invalid credentials"}, 401)

        token = jwt.encode({
            "username": user.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        }, "secret", algorithm="HS256")

        return make_response({"token": token})

