from app.extensions import ma
from app.models.channel import Channel

class ChannelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Channel
        load_instance = True
        
channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)