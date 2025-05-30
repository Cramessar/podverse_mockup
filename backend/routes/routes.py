from flask import Blueprint, jsonify

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/admin/dashboard", methods=["GET"])
def get_admin_dashboard():
    """
    Admin Dashboard endpoint
    ---
    responses:
      200:
        description: Dashboard info
        content:
          application/json:
            example:
              message: "Welcome Admin"
              user_count: 1234
              active_podcasts: 567
              site_uptime_days: 99.5
    """
    return jsonify({
        "message": "Welcome Admin",
        "user_count": 1234,
        "active_podcasts": 567,
        "site_uptime_days": 99.5,
    })

@routes_bp.route("/admin/users", methods=["GET"])
def list_users():
    """
    List recent users
    ---
    responses:
      200:
        description: List of users with basic info
        content:
          application/json:
            example:
              - id: 1
                email: user1@example.com
                joined: 2025-05-01
              - id: 2
                email: user2@example.com
                joined: 2025-05-10
    """
    return jsonify([
        {"id": 1, "email": "user1@example.com", "joined": "2025-05-01"},
        {"id": 2, "email": "user2@example.com", "joined": "2025-05-10"},
    ])

@routes_bp.route("/admin/podcasts", methods=["GET"])
def list_podcasts():
    """
    List active podcasts
    ---
    responses:
      200:
        description: List of podcasts with stats
        content:
          application/json:
            example:
              - id: 101
                title: Podverse Daily
                listeners: 12345
              - id: 102
                title: Tech Talk
                listeners: 6789
    """
    return jsonify([
        {"id": 101, "title": "Podverse Daily", "listeners": 12345},
        {"id": 102, "title": "Tech Talk", "listeners": 6789},
    ])

@routes_bp.route("/admin/stats/listening-trends", methods=["GET"])
def listening_trends():
    """
    Podcast listening trends
    ---
    responses:
      200:
        description: Listening trend data
        content:
          application/json:
            example:
              dates: ["2025-05-01", "2025-05-02", "2025-05-03"]
              listens: [100, 120, 95]
    """
    return jsonify({
        "dates": ["2025-05-01", "2025-05-02", "2025-05-03"],
        "listens": [100, 120, 95],
    })

@routes_bp.route("/admin/site-uptime", methods=["GET"])
def site_uptime():
    """
    Site uptime statistics
    ---
    responses:
      200:
        description: Uptime info
        content:
          application/json:
            example:
              uptime_days: 99.5
              last_downtime: "2025-04-30T14:00:00Z"
              downtime_duration_minutes: 15
    """
    return jsonify({
        "uptime_days": 99.5,
        "last_downtime": "2025-04-30T14:00:00Z",
        "downtime_duration_minutes": 15,
    })
