from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Performance,
    Play,
    TheatreHall,
    Genre,
    Actor,
    Ticket,
    Reservation,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id",
                  "name",
                  "rows",
                  "seats_in_row")


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ("id",
                  "title",
                  "description",
                  "actors",
                  "genres")


class PlayListSerializer(PlaySerializer):
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Play
        fields = ("id",
                  "title",
                  "description",
                  "actors",
                  "genres")


class PlayDetailSerializer(PlaySerializer):
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Play
        fields = ("id",
                  "title",
                  "description",
                  "actors",
                  "genres",)


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id",
                  "play",
                  "theatre_hall",
                  "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Performance
        fields = ("id",
                  "play_title",
                  "theatre_hall",
                  "show_time")


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlaySerializer()
    theatre_hall = TheatreHallSerializer()

    class Meta:
        model = Performance
        fields = ("id",
                  "play",
                  "theatre_hall",
                  "show_time")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id",
                  "row",
                  "seat",
                  "performance",
                  "reservation")


    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatre_hall,
        )
        return data


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id",
                  "created_at",
                  "tickets")

    @transaction.atomic
    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop('tickets')
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
        return reservation


class TheatreHallListSerializer(TheatreHallSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id",
                  "name",
                  "rows",
                  "seats_in_row")


class TheatreHallDetailSerializer(TheatreHallSerializer):
    performances = PerformanceListSerializer(many=True)

    class Meta:
        model = TheatreHall
        fields = ("id",
                  "name",
                  "rows",
                  "seats_in_row",
                  "performances")


class GenreListSerializer(GenreSerializer):
    class Meta:
        model = Genre
        fields = ("id",
                  "name")


class ActorListSerializer(ActorSerializer):
    class Meta:
        model = Actor
        fields = ("id",
                  "first_name",
                  "last_name")


class TicketListSerializer(TicketSerializer):
    pass


class ReservationListSerializer(ReservationSerializer):
    class Meta:
        model = Reservation
        fields = ("id",
                  "created_at",
                  "user")
