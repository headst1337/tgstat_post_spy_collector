from flask import jsonify
from . import bp


@bp.route('/init_scheduler', methods=['GET'])
def init_scheduler():

    from app.scheduler.scheduler import start_scheduler
    start_scheduler()
    return jsonify({"response": "scheduler started"})