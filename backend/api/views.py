from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

def test_message(request):
    """Dummy message to check if the backend and frontend can communicate"""
    return HttpResponse("Hello from the backend!")