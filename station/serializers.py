from rest_framework import serializers

from .models import Bus, Trip, Facility


# default drf serializer
class BusModelSerializer(serializers.Serializer):
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

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ('id', 'name', )

class BusSerializer(serializers.ModelSerializer):
    # do not set if you use __all__ in fields. Django understands it by his own
    is_small = serializers.ReadOnlyField()

    class Meta:
        model = Bus
        fields = ('id', 'info', 'num_seats', 'facilities', 'is_small')
        read_only_fields = ('id', )


class BusListSerializer(BusSerializer):
    facilities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'source', 'destination', 'departure', 'bus')


class TripListSerializer(TripSerializer):
    bus = BusSerializer()