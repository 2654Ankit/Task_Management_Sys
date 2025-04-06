# Task Manegement System


## Project overview 
### Models folder have three file 1. Task.py contain model of taskmanagger 2. TaskLogger.py container model of tasklogger and auditlog. 3. User.py contain model of Users
### app.py is in the root of project it is the main app which contain route(API).
### celery_app folder  contain a tasks folder having task.py file which conatain our periodic task performed by celery.
### celery_.py is the file which is in the root folder and contain instance of celery.
### extensions.py contain  Flask instance , database instance and redis instance.


#  RUN PROJECT ON DOCKER :-
## 1. PULL THE REPO
## 2. RUN  docker-compose up --build
## NOW YOU ARE LIVE GOTO POSTMAN AND HIT THE API FROM API REFERANCE SECTION BELOW






## Setup :-
### docker desktop is required so this must be on system. For installation refer https://docs.docker.com/desktop/setup/install/windows-install/
### Pull the repo 
### run :- 
#### - pip install -r requirements.txt   (install all the required package)
#### - docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest (this will install redis on docker.)
## To run project execute :-
### - flask run --port {port number}
## Invoke celery worker by executing 
### -  celery -A celery_ worker --pool=solo -l info
## invoke celery beat
### - celery -A celery_ beat --loglevel=info

## Now project is runnig 

# API REFERENCE :-
You have too provide a role:"admin" to any user so he can do authorized operations

### 1. Before executing any other operation you have to first signup (FOR ALL USERS FROM "admin" TO  "employee") run POST http://127.0.0.1:5000/signup  in format = {"username":"username","password":"password","role","role"}
### 2. Now login using http://127.0.0.1:5000/login  in format = {"usename":"username","pasword","password"} this will give a token use this token for all other curd operation using Postman. 
## CURD operations API :-
### 3. upload-csv file to taskmanager using http://127.0.0.1:5000/upload-csv  in format = {task_id,descriptions,status,priority,assigned_user}, Ensure all users are signuped.
### 4. List tasks filtered by date using GET http://127.0.0.1:5000/tasks?date=yyyy-mm-dd  
### 5. List all tasks from tasklogger using GET  http://127.0.0.1:5000/tasks
### 6. Retrieve task details from tasklogger using task_id run GET http://127.0.0.1:5000/tasks/<task_logger_id>
### 7. To create a task manually without csv file run POST  http://127.0.0.1:5000/create_task and give data in format = {task_id,descriptions,status,priority,assigned_user}
### 8. Update a task status as TRUE or FALSE run PUT http://127.0.0.1:5000/task/<task_id> example :- {"status":"TRUE"}
### 9. To Soft delete a task (mark as inactive/FALSE) run DELETE http://127.0.0.1:5000/task/<task_id> , this will not delete the task only make task staus FALSE and can only done by admin.
### Delete a task in taskmanagger it will cascade delete operation run DELETE  http://127.0.0.1:5000/delete_task/<task_id>, THIS OPERATION CAN ONLY DONE BY "admin".
