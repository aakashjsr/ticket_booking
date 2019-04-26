from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib import messages

from .models import Seat
from .utils import get_user, send_booking_email
from .forms import TicketForm


class IndexView(TemplateView):
    """
    Renders the home page for the app.
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return {"seats": Seat.objects.all().order_by("id")}


class BookSeatView(View):
    """
    Handles ticket booking for users.
    """

    def post(self, request):
        home_url = reverse("index")
        form = TicketForm(request.POST)

        # render error if form parameters are not correct
        if not form.is_valid():
            messages.error(request, "Invalid booking data.")
            return HttpResponseRedirect(home_url)

        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["name"]
        seat_id = form.cleaned_data["seat"]
        user = get_user(email, first_name)

        # If user has already booked seat then throw error
        if user.seats.count() > 0:
            messages.error(request, "You can book only one seat.")
            return HttpResponseRedirect(home_url)

        # Try to book seat
        seat = Seat.objects.get(id=seat_id)
        if seat.book_seat(user):
            # TODO: move this to background job
            seat.refresh_from_db()
            send_booking_email(seat)
            messages.success(request, "Your seat has been successfully booked.")
            return HttpResponseRedirect(home_url)
        else:
            # Booking failed as some other booked it concurrently
            messages.error(request, "This seat is no longer available.")
            return HttpResponseRedirect(home_url)
