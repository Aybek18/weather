from django.urls import path

from weathers.views import WeatherAPIView

urlpatterns = [
    path("", WeatherAPIView.as_view(), name="weather")
]