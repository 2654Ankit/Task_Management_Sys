from services.logger_service import LoggerService

logger_service = LoggerService()

def get_task_from_tasklogger(current_user, task_logger_id):
    return logger_service.get_task(task_logger_id)