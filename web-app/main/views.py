from django.shortcuts import render


def index(request):
    """The app's home page."""
    # This could just be a static page (using TemplateView)
    # instead of a rendered template.
    return render(request, "main/index.html")
