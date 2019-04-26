# Generated by Django 2.2 on 2019-04-23 13:49

from django.db import migrations


def seed_initial_data(apps, schema_editor):
    """
    Creates 30 seats when the app is initialized
    """
    seat = apps.get_model("seats", "Seat")
    seats_data = [seat() for index in range(30)]
    seat.objects.bulk_create(seats_data)


class Migration(migrations.Migration):

    dependencies = [("seats", "0001_initial")]

    operations = [migrations.RunPython(seed_initial_data, migrations.RunPython.noop)]
