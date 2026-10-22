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

@bp.get("")
def get_all_tasks():

    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

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

@bp.patch("/<task_id>/mark_complete")
def patch_task_mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.mark_complete()

    db.session.commit()

    return make_response("", 204, {"Content-Type" : "application/json"})

@bp.patch("/<task_id>/mark_incomplete")
def patch_task_mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.mark_incomplete()

    db.session.commit()

    return make_response("", 204, {"Content-Type" : "application/json"})