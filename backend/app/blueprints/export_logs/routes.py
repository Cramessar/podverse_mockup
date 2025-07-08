# backend/app/blueprints/export_logs/routes.py

from flask import jsonify, request, send_file
from sqlalchemy import and_, or_, desc
from . import export_logs_bp
from app.extensions import limiter, db
from app.models.export_logs import ExportLog
from app.utils.error_exceptions import NotFoundError, ValidationError
from app.utils.auth import requires_auth
from app.utils.logger import get_logger, log_request_start, log_request_end
from app.utils.query_params import get_pagination_params, get_sorting_params
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

        # Build query
        query = ExportLog.query

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

        # Apply date range filter if provided
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
        sort_column = getattr(ExportLog, sort_by)
        if sort_order == 'desc':
            sort_column = desc(sort_column)
        query = query.order_by(sort_column)

        # Execute paginated query
        paginated_logs = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Serialize results
        logs = [export_log_schema.dump(log) for log in paginated_logs.items]

        return jsonify({
            'logs': logs,
            'total': paginated_logs.total,
            'pages': paginated_logs.pages,
            'current_page': paginated_logs.page,
            'per_page': paginated_logs.per_page
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
        # Get the export log
        log = ExportLog.query.get(log_id)
        if not log:
            raise NotFoundError("Export log not found")

        # Check if file exists
        if not log.file_path or not os.path.exists(log.file_path):
            raise NotFoundError("Export file not found or has expired")

        # Get filename from path
        filename = os.path.basename(log.file_path)

        # Send file securely
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


