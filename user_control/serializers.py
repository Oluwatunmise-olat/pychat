from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({'password': 'password mismatch'})
        return data
