from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Bus, Trip, Facility, Order, Ticket


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
    buses = SlugRelatedField(many=True, read_only=True, slug_field='info')
    class Meta:
        model = Facility
        fields = ('id', 'name', 'buses')

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
    tickets = serializers.ReadOnlyField(source='tickets.count')

    class Meta:
        model = Trip
        fields = ('id', 'source', 'destination', 'departure', 'bus', 'tickets')


class TripListSerializer(TripSerializer):
    bus_info = serializers.ReadOnlyField(source='bus.info')
    bus_seats = serializers.ReadOnlyField(source='bus.num_seats')

    class Meta(TripSerializer.Meta):
        fields = ('id', 'source', 'destination', 'departure', 'tickets', 'bus_info', 'bus_seats')


class TripRetrieveSerializer(TripSerializer):
    bus = BusListSerializer()


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'seat', 'trip')
        """
        django support UniqueConstraint and unique_together from model constraints,
        it create UniqueTogetherValidator automatically
        """
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=('seat', 'trip')
            )
        ]

    # custom serializer validation
    def validate(self, attrs):
        Ticket.validate_seat(
            seat_num=attrs['seat'],
            bus_num_seats=attrs['trip'].bus.num_seats,
            exception_to_raise=serializers.ValidationError
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'tickets')


    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop('tickets')

            order = Order.objects.create(**validated_data)

            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)

            return order
