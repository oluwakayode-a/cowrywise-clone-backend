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
        fields = ("amount", "plan_id")


class TransferBankAccountSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    recipient = serializers.CharField()
    reference = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"