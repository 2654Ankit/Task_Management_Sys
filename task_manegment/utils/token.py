# import jwt
# from functools import wraps
# from flask import request, jsonify
# from Models.User import Users

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get("Authorization")
#         if not token:
#             return jsonify({"message": "Token is missing!"}), 401
#         try:
#             data = jwt.decode(token, "secret", algorithms=["HS256"])
#             current_user = Users.query.filter_by(username=data["username"]).first()
#         except Exception as e:
#             return jsonify({"message": "Token is invalid!"}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated













import jwt
from functools import wraps
from flask import request, jsonify
from Models.User import Users

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(username=data["username"]).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

