from django.urls import path

from .views import BookSeatView


urlpatterns = [path("book/", BookSeatView.as_view(), name="book")]
