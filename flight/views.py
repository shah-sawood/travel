"""all backend goes here"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Flight, Passenger, Airport

# Create your views here.
def index(request):
    """displays all flights on home page"""
    flight = Flight.flights.filter(departing_time__gt=timezone.now()).first()
    context = {
        "flight": flight,
        "title": "home",
    }
    return render(request, "flight/index.html", context)


def get_flight(request, flight_id):
    """tries to display a specific flight"""
    try:
        flight = Flight.flights.get(pk=flight_id, departing_time__gt=timezone.now())
    except Flight.DoesNotExist:
        return render(
            request,
            "flight/error.html",
            {
                "message": "The request flight does not exist.\
                It might have been deleted or departed.",
            },
        )
    else:
        context = {
            "flight": flight,
            "title": f"{flight} ({flight.get_passengers().count()})",
        }
        return render(request, "flight/flight.html", context)


def get_flights(request):
    """display the page of the flights which are not departed yet"""
    context = {}
    context["flights"] = Flight.flights.filter(departing_time__gt=timezone.now())
    context["title"] = "flights"
    return render(request, "flight/flights.html", context)


@login_required
@require_POST
def book(request, flight_id):
    """adds a passenger to flight of flight_id"""

    try:
        flight = Flight.flights.get(pk=flight_id)
        passenger_id = int(request.POST.get("passenger"))
        passenger = Passenger.passengers.get(pk=passenger_id)
        if not passenger.flights.contains(flight):
            passenger.flights.add(flight)
            passenger.cash -= flight.get_price()
            passenger.save()
    except (Flight.DoesNotExist, ValueError, Passenger.DoesNotExist):
        return render(
            request,
            "flight/error.html",
            {
                "message": "Something went wrong. Please try again later.",
            },
        )
    else:
        return HttpResponseRedirect(reverse("flights"))


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
