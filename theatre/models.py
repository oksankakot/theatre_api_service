from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class TheatreHall(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=63)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.DO_NOTHING, related_name="performances")
    show_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.play}, {self.theatre_hall.name}, {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)


class TicketManager(models.Manager):
    def validate_ticket(self, row, seat, performance):
        theatre_hall = performance.theatre_hall

        max_row = theatre_hall.rows
        max_seat = theatre_hall.seats_in_row

        if not (1 <= row <= max_row and 1 <= seat <= max_seat):
            raise ValidationError(
                f"Number of row and seat must be in diapason (1, {max_row}) and (1, {max_seat}) respectively."
            )

        if self.filter(performance=performance, row=row, seat=seat).exists():
            raise ValidationError(
                "The selected row and seat are already occupied for this performance."
            )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.DO_NOTHING, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    objects = TicketManager()

    def clean(self):
        performance = self.performance
        if isinstance(performance, Performance):
            theatre_hall = performance.theatre_hall
            if isinstance(theatre_hall, TheatreHall):
                Ticket.objects.validate_ticket(self.row, self.seat, performance)

    def save(self, *args, **kwargs):
        if not self.id:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.performance} (row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]
