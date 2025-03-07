from rest_framework import serializers

class GoogleDocSerializer(serializers.Serializer):
    content = serializers.CharField()
