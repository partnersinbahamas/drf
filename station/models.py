from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField("Facility", related_name='buses')

    class Meta:
        verbose_name_plural = "Buses"
        verbose_name = "Bus"

    @property
    def is_small(self):
        return self.num_seats < 30

    def __str__(self):
        return f"Bus {self.info} - ({self.id})"


class Trip(models.Model):
    source = models.CharField(max_length=63)
    destination = models.CharField(max_length=63)
    departure = models.DateTimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="trips")

    def __str__(self):
        return f"Bus({self.bus.pk}) from {self.source} to {self.destination}."

    class Meta:
        indexes = [
            models.Index(fields=['source', 'destination'], name='source_destination_idx'),
            models.Index(fields=['departure'], name='departure_idx'),
        ]


class Ticket(models.Model):
    seat = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"{self.trip} - seat: {self.seat}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['seat', 'trip'], name='unique_seat_trip'),
        ]

    @staticmethod
    def validate_seat(seat_num: int, bus_num_seats: int, exception_to_raise) -> None:
        if seat_num < 1:
            raise exception_to_raise({"min_value": "Seat must be greater than 1."})

        if seat_num > bus_num_seats:
            raise exception_to_raise({"seat_range": "Seat must be in bus num_seats range."})

    def clean(self):
        self.validate_seat(self.seat, self.trip.bus.num_seats, ValidationError)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.created_at)


class Facility(models.Model):
    name = models.CharField(max_length=85, unique=True)

    class Meta:
        verbose_name_plural = "Facilities"
        verbose_name = "Facility"

    def __str__(self):
        return self.name
