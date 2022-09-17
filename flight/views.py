"""all backend goes here"""
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Flight, Passenger, Airport

# Create your views here.
def index(request):
    """displays all flights on home page"""
    flights = Flight.flights.all()
    context = {
        "flights": flights,
        "title": "home",
    }
    return render(request, "flight/index.html", context)


@login_required
def get_flight(request, flight_id):
    """displays specific flight"""
    flght = Flight.flights.get(pk=flight_id)
    passengers = flight.passengers.all()
    context = {
        "flight": flight,
        "passengers": passengers,
    }
    return render(request, "flight/flight.html", context)


def get_flights(request):
    """display the page of the flights"""
    context = {}
    context["flights"] = Flight.flights.all()
    context["title"] = "flights"
    return render(request, "flight/flights.html", context)


def book(request, flight_id):
    """adds a passenger to flight of flight_id"""

    flight = Flight.flights.get(pk=flight_id)
    non_passengers = models.Passenger.objects.exclude(flights=flight).all()
    context = {"flight": flight, "non_passengers": non_passengers}

    if request.method == "POST":
        try:
            passenger_id = int(request.POST.get("passenger"))
            passenger = models.Passenger.objects.get(pk=passenger_id)
            passenger.flights.add(flight)
            return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
        except (ValueError, models.Passenger.DoesNotExist):
            context["message"] = "Something went wrong. Please try again later."
    return render(request, "flights/book.html", context)


def add_flight(request):
    airports = models.Airport.objects.all()
    context = {"airports": airports, "title": "Add Flight"}

    # when method is post
    if request.method == "POST":
        _from = request.POST.get("from")
        _to = request.POST.get("to")
        _duration = request.POST.get("duration")

        origin = models.Airport.objects.get(id=_from)
        destination = models.Airport.objects.get(id=_to)

        # check whether destination and origin are same or not
        if origin.id == destination.id:
            context["message"] = "Origin and destination can't be same."
            return render(request, "flights/add_flight.html", context)

        # check if flight from "origin" to "destination" exists or not
        try:
            flight = Flight.flights.get(origin=origin, destination=destination)
            context["message"] = "<h1>Fligth from {} to {} already exist.</h1>".format(
                origin, destination
            )
            return render(request, "flights/add_flight.html", context)
        except (models.Flight.DoesNotExist, models.Flight.MultipleObjectsReturned):
            pass

        created_flight = Flight.flights.create(
            origin=origin, destination=destination, duration=_duration
        )

        return HttpResponseRedirect(reverse("flights:index"))

    # when method is not post
    return render(request, "flights/add_flight.html", context)


def generate_name(number_of_names=10):
    names = []
    alphabets = list(ascii_lowercase)
    for i in range(number_of_names):
        name = ""
        for j in range(7):
            name += random.choice(alphabets)
        names.append(name.title())

    return names
