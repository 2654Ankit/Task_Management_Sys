from flask import request
from services.task_service import TaskService

task_service = TaskService()

def upload_csv(current_user):
    return task_service.upload_csv(current_user, request)

def create_task(current_user):
    return task_service.create_task(current_user, request.get_json())

def modify_task(current_user, task_id):
    return task_service.modify_task(current_user, task_id, request.get_json())

def update_status(current_user, task_id):
    return task_service.update_status(current_user, task_id, request.get_json())

def get_tasks():
    return task_service.get_tasks(request)

