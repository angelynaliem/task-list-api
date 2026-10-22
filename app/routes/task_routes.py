from flask import Blueprint, make_response, request
from ..models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db
import os, requests

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
    notify_slack(task.title)

    return make_response("", 204, {"Content-Type" : "application/json"})

@bp.patch("/<task_id>/mark_incomplete")
def patch_task_mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.mark_incomplete()

    db.session.commit()

    return make_response("", 204, {"Content-Type" : "application/json"})

def notify_slack(task_title):
    token = os.environ.get("SLACK_BOT_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    body = {
    "channel": "task-notifications-c26",
    "text": f"Someone just completed the task {task_title}"
    }
    response = requests.post("https://slack.com/api/chat.postMessage", 
    headers=headers, 
    json=body
    )
    # print("Slack Response Status:", response.status_code)
    # print("Slack Response JSON:", response.json())
