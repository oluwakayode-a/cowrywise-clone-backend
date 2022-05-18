from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"