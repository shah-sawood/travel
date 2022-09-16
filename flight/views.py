"""all backend goes here"""
from django.shortcuts import render

# Create your views here.
def index(request):
    """displays landing page of the application"""
    context = {}
    return render(request, "flight/index.html", context)
