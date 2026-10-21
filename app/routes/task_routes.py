from flask import Blueprint, abort, make_response, request, Response
from ..models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        response = {
            "details": "Invalid data"
        }
        return response, 400
    
    return create_model(Task, request_body)
    
    # title = request_body["title"]
    # description = request_body["description"]
    # completed_at = request_body.get("completed_at")

    # new_task = Task(title=title, description=description, completed_at=completed_at)

    # db.session.add(new_task)
    # db.session.commit()

    # response = new_task.to_dict()
    # response = {
    #     "id" : new_task.id,
    #     "title" : new_task.title,
    #     "description" : new_task.description,
    #     "is_complete" : new_task.completed_at is not None
    # }
    
    # return response, 201

@bp.get("")
def get_all_tasks():
    # query = db.select(Task).order_by(Task.id)
    # tasks = db.session.scalars(query)
    # tasks_response = []
    # for task in tasks:
    #     tasks_response.append(
    #         {
    #             "id": task.id,
    #             "title": task.title,
    #             "description": task.description,
    #             "is_complete": task.completed_at is not None
    #         }
    #     )
    # return tasks_response
    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

    # return {
    #     "id" : task.id,
    #     "title" : task.title,
    #     "description" : task.description,
    #     "is_complete" : task.completed_at is not None
    # }

# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         response = {"message" : f"task {task_id} is invalid"}
#         abort(make_response(response, 400))

#     query = db.select(Task).where(Task.id == task_id)
#     task = db.session.scalar(query)

#     if not task:
#         response = {"message" : f"task {task_id} is not found"}
#         abort(make_response(response, 404))
    
#     return task

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response("", 204)

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response("", 204)
