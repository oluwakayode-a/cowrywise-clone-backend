from rest_framework import serializers

class StashSerializer(serializers.Serializer):
    amount = serializers.IntegerField()

    class Meta:
        fields = "__all__"


class TransferStashSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    reference = serializers.CharField()

    class Meta:
        fields = "__all__"