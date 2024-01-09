from rest_framework import serializers

from weathers.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = (
            "city",
            "temperature",
            "pressure",
            "wind_speed"
        )
