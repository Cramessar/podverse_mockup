# backend/app/blueprints/export_logs/schemas.py

from marshmallow import fields, validate
from app.extensions import ma
from app.models.export_logs import ExportLog

class ExportLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExportLog
        load_instance = True
        include_fk = True

    # Add explicit field definitions for validation and formatting
    id = fields.Integer(dump_only=True)
    admin_email = fields.Email(required=True)
    export_type = fields.String(required=True, validate=validate.OneOf(['channels', 'feeds', 'items']))
    filters = fields.Dict(keys=fields.String(), values=fields.Raw(), required=False)
    status = fields.String(required=True, validate=validate.OneOf(['pending', 'success', 'failed', 'skipped', 'expired']))
    file_path = fields.String(allow_none=True)
    format = fields.String(required=True, validate=validate.OneOf(['csv', 'json']))
    channels_count = fields.Integer(allow_none=True)
    feeds_count = fields.Integer(allow_none=True)
    items_count = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(allow_none=True)
    error_message = fields.String(allow_none=True)

    # Add computed fields
    duration = fields.Method("get_duration")
    is_expired = fields.Method("get_is_expired")
    has_file = fields.Method("get_has_file")

    def get_duration(self, obj):
        """Calculate duration of export in seconds"""
        if obj.completed_at and obj.created_at:
            return (obj.completed_at - obj.created_at).total_seconds()
        return None

    def get_is_expired(self, obj):
        """Check if export file has expired (older than 30 days)"""
        if obj.created_at:
            from datetime import datetime, timedelta
            return datetime.utcnow() - obj.created_at > timedelta(days=30)
        return False

    def get_has_file(self, obj):
        """Check if export file exists"""
        import os
        return bool(obj.file_path and os.path.exists(obj.file_path))

# Create schema instances
export_log_schema = ExportLogSchema()
export_logs_schema = ExportLogSchema(many=True)