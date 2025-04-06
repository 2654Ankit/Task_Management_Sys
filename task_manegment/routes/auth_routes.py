from flask import Blueprint
from controller.auth_controller import signup, login

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/signup", methods=["POST"])(signup)
auth_bp.route("/login", methods=["POST"])(login)