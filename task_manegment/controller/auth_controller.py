from flask import request
from services.auth_service import AuthService

auth_service = AuthService()

def signup():
    data = request.get_json()
    return auth_service.signup(data)

def login():
    data = request.get_json()
    return auth_service.login(data)