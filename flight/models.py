"""model of flight application"""
from django.db import models


# Create your models here.
class Airport(models.Model):
    """airport model"""

    code = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=64, unique=True)

    airports = models.Manager()

    def get_id(self):
        """returns id of this airport"""
        return self.id

    def get_city(self):
        """returns city of this airport"""
        return self.city

    def get_city_code(self):
        """returns the city code of this airport"""
        return self.code

    def __str__(self):
        """returns the string representation of this airport"""
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    """flight model"""

    origin = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departures"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrivals"
    )
    duration = models.PositiveIntegerField()
    departing_time = models.DateTimeField()
    picture = models.ImageField(upload_to="flight/images/")

    flights = models.Manager()

    def get_id(self):
        """returns id of this airport"""
        return self.id

    def get_origin(self):
        """returns the origin of the flight"""
        return self.origin

    def get_passengers(self):
        """returns a list of passengers on the flight"""
        return self.passengers

    def get_num_of_passengers(self):
        """returns a list of passengers on the flight"""
        return self.get_passengers().count()

    def get_destination(self):
        """returns the destination of the flight"""
        return self.destination

    def get_duration(self):
        """returns the duration of the flight"""
        return self.duration

    def get_departing_time(self):
        """returns the departing_time of the flight"""
        return self.departing_time

    def __str__(self):
        """returns the string representation of this airport"""
        return f"{self.origin} to {self.destination}"

    def is_valid_flight(self):
        """checks whether a flight is valid or not"""
        return self.origin != self.destination and self.duration > 0


class Passenger(models.Model):
    """passenger model"""

    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    cnic = models.PositiveIntegerField()
    flights = models.ManyToManyField(
        Flight,
        blank=True,
        related_name="passengers",
    )

    passengers = models.Manager()

    def __str__(self):
        """returns the string representation of this airport"""
        return f"{self.first}, {self.last}"

    def get_id(self):
        """returns id of this airport"""
        return self.id
