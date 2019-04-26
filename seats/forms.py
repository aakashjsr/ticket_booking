from django import forms


class TicketForm(forms.Form):
    """
    Form to validate ticket form submitted by UI
    """

    email = forms.EmailField(max_length=255)
    name = forms.CharField(max_length=255)
    seat = forms.CharField(max_length=10)
