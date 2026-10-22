from flask import Blueprint, make_response, request
from ..models.goal import Goal
from ..routes.route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        response = {
            "details" : "Invalid data"
        }
    
        return response, 400

    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():

    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response("", 204, {"Content-Type" : "application/json"})

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response("", 204)

