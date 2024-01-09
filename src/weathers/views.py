from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weathers.serializers import WeatherSerializer
from weathers.services import WeatherService


# Create your views here.
class WeatherAPIView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="city", location=OpenApiParameter.QUERY,
                required=True, type=str
            ),
        ],
        responses={201: OpenApiResponse()}
    )
    def get(self, request, *args, **kwargs):
        converted_currencies = WeatherService.factory().retrieve_weather(city_name=request.query_params.get("city"))

        return Response(data=WeatherSerializer(converted_currencies).data, status=status.HTTP_200_OK)
