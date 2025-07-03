from flask import Blueprint, request, jsonify
from ai.backend.utils.report_generator import generate_report

report_bp = Blueprint("report", __name__)

@report_bp.route("/report/<int:channel_id>", methods=["GET"])
def get_report(channel_id):
    model = request.args.get("model", "mistral")
    report_md = generate_report(channel_id, model)
    return jsonify({"report": report_md})
