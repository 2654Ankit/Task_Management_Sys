from flask import Blueprint
from controller.logger_controller import get_task_from_tasklogger
from utils.token import token_required

logger_bp = Blueprint("logger", __name__)

logger_bp.route("/task/<task_logger_id>", methods=["GET"])(token_required(get_task_from_tasklogger))
