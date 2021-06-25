from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from .models import Stops

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


def test_message(request):
    """Dummy message to check if the backend and frontend can communicate"""
    return HttpResponse("Hello from the backend!")


def test_db(request):
    """Dummy message to check if the database is integrated successfully"""
    stop = Stops.objects.all();
    return HttpResponse(stop)