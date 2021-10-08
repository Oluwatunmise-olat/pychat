from rest_framework.serializers import ModelSerializer

from chat_control.models import Message


class PreviousMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('thread', 'sender', 'recipient', 'content', 'created')
