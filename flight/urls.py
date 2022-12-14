"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from . import views

flights = [
    path("book/<int:flight_id>/", views.book, name="book"),
    path("<int:flight_id>/", views.get_flight, name="flight"),
    path("", views.get_flights, name="flights"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("flights/", include(flights)),
    path("logout/", LogoutView.as_view(), name="logout"),
]
