from rest_framework import serializers

from .models import Bus

class BusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    info = serializers.CharField(required=False, max_length=255)
    num_seats = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Bus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.info = validated_data.get('info', instance.info)
        instance.num_seats = validated_data.get('num_seats', instance.num_seats)
        instance.save()

        return instance