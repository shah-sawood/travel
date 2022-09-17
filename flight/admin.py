from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Flight)
class FlightAdmin(admin.ModelAdmin):
    list_dispaly = ["origin", "destination"]


@admin.register(models.Passenger)
class PassengerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Airport)
class AirportAdmin(admin.ModelAdmin):
    pass
