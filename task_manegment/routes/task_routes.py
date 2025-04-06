from flask import Blueprint
from controller.task_controller import upload_csv, create_task, modify_task, update_status, get_tasks
from utils.token import token_required

task_bp = Blueprint("task", __name__)

task_bp.route("/upload-csv", methods=["POST"])(token_required(upload_csv))
task_bp.route("/create_task", methods=["POST"])(token_required(create_task))
task_bp.route("/task/<task_id>", methods=["PUT"])(token_required(modify_task))
task_bp.route("/task/<task_id>", methods=["DELETE"])(token_required(update_status))
task_bp.route("/tasks", methods=["GET"])(get_tasks)