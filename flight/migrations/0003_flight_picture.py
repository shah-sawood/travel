# Generated by Django 4.1 on 2022-09-17 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0002_flight_departing_time_passenger_cnic"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="picture",
            field=models.ImageField(
                default="flight/images/1.jpg", upload_to="flight/images/"
            ),
            preserve_default=False,
        ),
    ]