# app/blueprints/channel/routes.py

from . import channel_bp
from app.blueprints.channel.controller import list_channels, get_channel_by_id, export_channels
from app.utils.auth import requires_auth
from app.extensions import limiter


@channel_bp.route('', methods=['GET'])
@limiter.limit("30 per minute")
@requires_auth
def get_all_channels():
    return list_channels()


@channel_bp.route('/export', methods=['GET'])
@limiter.limit("10 per minute")  # Lower rate limit for exports?
@requires_auth
def export_channels_route():
    return export_channels()


@channel_bp.route('/<int:channel_id>', methods=['GET'])
@limiter.limit("60 per minute")
@requires_auth
def get_single_channel(channel_id):
    return get_channel_by_id(channel_id)
