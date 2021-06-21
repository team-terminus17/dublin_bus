"""
from django.conf import settings
from django.conf.urls.static import static

# We aren't using django templates at the moment.
urlpatterns = []

# A development-only entry point to static files.
# In production, this should be handled by heroku configuration.
if settings.DEBUG:
    urlpatterns += static("/", document_root=settings.STATIC_ROOT, path="main/index.html")
"""


from django.conf.urls import include, url
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.generic import RedirectView

urlpatterns = [

    # / routes to index.html
    url(r'^$', serve, kwargs={'path': 'main/index.html'}),

    # static files (*.css, *.js, *.jpg etc.) served on /
    # (assuming Django uses /static/ and /media/ for static/media urls)
    url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
        RedirectView.as_view(url='/static/main/%(path)s', permanent=False)),

]
