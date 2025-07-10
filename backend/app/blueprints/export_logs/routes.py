# backend/app/blueprints/export_logs/routes.py

from flask import jsonify, request, send_file
from sqlalchemy import and_
from . import export_logs_bp
from app.extensions import limiter, db
from app.models.export_logs import ExportLog
from app.utils.error_exceptions import NotFoundError, ValidationError
from app.utils.auth import requires_auth
from backend.app.utils.request_logger import get_logger
from app.utils.query_params import get_pagination_params, get_sorting_params
from app.utils.query_helpers import paginate_query, apply_sorting
from app.blueprints.export_logs.schemas import export_log_schema
import os

logger = get_logger(__name__)

@export_logs_bp.route('/', methods=['GET'])
#@requires_auth
@limiter.limit("100 per day")
def get_export_logs():
    """Get paginated list of export logs. Supports filtering, pagination, status checks"""
    try:
        # Get pagination and sorting parameters
        page, per_page = get_pagination_params(request)
        sort_by, sort_order = get_sorting_params(
            request,
            ['created_at', 'completed_at', 'status', 'export_type'],
            default_field='created_at'
        )

        query = db.session.query(ExportLog)

        # Apply filters
        status = request.args.get('status')
        if status:
            query = query.filter(ExportLog.status == status)

        export_type = request.args.get('export_type')
        if export_type:
            query = query.filter(ExportLog.export_type == export_type)

        admin_email = request.args.get('admin_email')
        if admin_email:
            query = query.filter(ExportLog.admin_email == admin_email)

        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            query = query.filter(
                and_(
                    ExportLog.created_at >= start_date,
                    ExportLog.created_at <= end_date
                )
            )

        # Apply sorting
        query = apply_sorting(query, ExportLog, sort_by, sort_order)

        # Paginate
        logs, pagination_metadata = paginate_query(query, page, per_page)

        return jsonify({
            'logs': [export_log_schema.dump(log) for log in logs],
            **pagination_metadata
        })

    except Exception as e:
        logger.error(f"Error retrieving export logs: {str(e)}")
        raise ValidationError(f"Failed to retrieve export logs: {str(e)}")


@export_logs_bp.route('/<int:log_id>/download', methods=['GET'])
#@requires_auth
@limiter.limit("50 per day")
def download_export_file(log_id):
    """Download the exported file for a specific log"""
    try:
        log = db.session.get(ExportLog, log_id)
        if not log:
            raise NotFoundError("Export log not found")

        if not log.file_path or not os.path.exists(log.file_path):
            raise NotFoundError("Export file not found or has expired")

        filename = os.path.basename(log.file_path)

        return send_file(
            log.file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv' if log.format == 'csv' else 'application/json'
        )

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error downloading export file: {str(e)}")
        raise ValidationError(f"Failed to download export file: {str(e)}")
