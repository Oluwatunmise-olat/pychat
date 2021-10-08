

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
