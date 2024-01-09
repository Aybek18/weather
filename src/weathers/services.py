from dataclasses import dataclass
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from core.services import BaseWeatherIntegration
from weathers.models import Weather


@dataclass
class WeatherIntegration(BaseWeatherIntegration):
    base_url = settings.INTEGRATION_BASE_URL
    timeout = settings.INTEGRATION_TIMEOUT
    api_key = settings.INTEGRATION_API_KEY

    def get_weather(self, city_name: str) -> dict:
        url = f"{self.base_url}/data/2.5/weather?q={city_name}&units=Metric&appid={self.api_key}"
        response = self._get(url=url, timeout=self.timeout)
        return {"result": response.json()}


@dataclass
class WeatherService:
    weather_integration: WeatherIntegration

    def retrieve_weather(self, city_name: str) -> Weather:
        existing_city = Weather.objects.filter(city=city_name).first()
        now = timezone.now()

        if not existing_city or existing_city.last_updated < now - timedelta(minutes=30):
            return self.save_weather(city_name=city_name, now=now)

        return existing_city

    def save_weather(self, city_name: str, now: datetime) -> Weather:
        new_city = self.weather_integration.get_weather(city_name=city_name)

        weather_data = new_city.get("result") or {}
        main_data = weather_data.get("main") or {}
        wind_data = weather_data.get("wind") or {}

        temperature = main_data.get("temp")
        pressure = main_data.get("pressure")
        wind_speed = wind_data.get("speed")

        instance, created = Weather.objects.update_or_create(
            city=city_name,
            defaults={
                'temperature': temperature,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'last_updated': now
            }
        )
        return instance

    @classmethod
    def factory(cls) -> "WeatherService":
        return cls(WeatherIntegration.factory())
