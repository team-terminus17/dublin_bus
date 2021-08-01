"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.urls import path, include, re_path

from .api.views import *

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('routes', get_routes, name='routes'),
    path('stops/<stop>/<int:direction>', get_stops, name='stops'),
    path('stop/<int:stop>/coordinates', get_stop_coordinates, name='stop_position'),
    path('coordinate/<int:direction>/<route>/<int:stop_dep>/<int:stop_arr>', get_coordinates, name='coordinate'),
    path('predict/<route>/<int:direction>/<int:dep_stop>/<int:arr_stop>/<int:datetime>', predict_time, name='predict'),
    path('weather', get_weather, name='weather'),
    path('ptpjourney', get_journey_time, name='journey'),
    path('stops/<agency>/<route>/info', get_stop_info, name='stop info'),
    path('shape/<route>/<int:direction>/<int:dep_stop>/<int:arr_stop>', get_shape, name='shape'),
    path('trips/<agency>/<route>/current', get_bus_positions, name="trips"),
    re_path(r'^(?P<worker_name>manifest).json$', serve_worker_view, name='manifest'),
    re_path(r'^(?P<worker_name>[-\w\d.]+).js$', serve_worker_view, name='serve_worker'),
    re_path(r'^(?P<worker_name>robots).txt$', serve_worker_view, name='robots'),
]
