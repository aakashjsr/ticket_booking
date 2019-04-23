from django.db import models, transaction
from django.contrib.auth.models import User


class Seat(models.Model):
    """
    Database model for seats
    """

    BOOKED = "booked"
    AVAILABLE = "available"

    booked_by = models.ForeignKey(
        User, related_name="seats", on_delete=models.SET_NULL, null=True, blank=True
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=25, choices=[(BOOKED, BOOKED), (AVAILABLE, AVAILABLE)],
        default=AVAILABLE
    )
    version = models.BigIntegerField(default=0)

    def __str__(self):
        """
        Formats display name for seat
        :return: string - seat's representation
        """
        return "Seat {} ({})".format(self.id, self.status)

    @transaction.atomic
    def book_seat(self, user):
        """
        Books seats selected by user while handling concurrent booking using optimistic lock in
        :param user: user instance booking the seat
        :return: Boolean - Indicating whether the booking was successful
        """
        current_version = self.version
        updated_rows = Seat.objects.filter(
            id=self.id, status=self.AVAILABLE, version=current_version
        ).update(booked_by=user, status=self.BOOKED, version=current_version + 1)
        return updated_rows > 0

    def clear_seat(self):
        """
        Clear the booked seats
        :return:
        """
        self.status = self.AVAILABLE
        self.save()
