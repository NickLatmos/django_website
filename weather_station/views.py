from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weather as WeatherModel, Valve as ValveModel
from .serializer import WeatherSerializer
import datetime

class Weather(APIView):
  '''
  Return all the weather measurements for the specified weather station
  Posts new weather data from the specified weather station (if valid)
  GET url: http://127.0.0.1:8000/weather_station/<ID>
  POST url http://127.0.0.1:8000/weather_station/
  '''

  # GET method To be deleted. 
  def get(self, request, weather_station_id):
    try: 
      weather = WeatherModel.objects.filter(ID=weather_station_id)
      if not weather:
        raise Http404
      serializer = WeatherSerializer(weather, many=True)          # When using filter() we must include many=True
      return Response(serializer.data)
    except WeatherModel.DoesNotExist:
      raise Http404

  def post(self, request, format=None):
    serializer = WeatherSerializer(data=request.data)
    # If the posted weather station's ID is not equal to anyone from the database then reject it.
    if serializer.is_valid():
      serializer.save()
      return (Response('Data successfully posted %c' % '\a', status=status.HTTP_201_CREATED))
    return (Response('Something went wrong %c' % '\a', status=status.HTTP_400_BAD_REQUEST))

class WeatherToday(APIView):
  '''
  Returns the weather measurements taken today
  url: http://127.0.0.1:8000/weather_station/today/<ID>
  '''
  def get(self, request, weather_station_id):
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather = weather.filter(date=datetime.date.today())
    if not weather:
      raise Http404
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)

class WeatherLastDays(APIView):
  '''
  Returns the weather measurements in the last <days> days
  url: http://127.0.0.1:8000/weather_station/<ID>/days/<days>
  '''
  def get(self, request, weather_station_id, days):
    date_threshold = datetime.date.today() - datetime.timedelta(days=int(days))
    date = datetime.date.today()
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather = weather.filter(date__gte=date_threshold)
    if not weather:
      raise Http404
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)

class WeatherSpecificMonth(APIView):
  '''
  Returns the weather measurements for the month <month> (in decimal represantation)
  url: http://127.0.0.1:8000/weather_station/<ID>/month/<month>/
  '''
  def get(self, request, weather_station_id, month):
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather = weather.filter(date__month=month)
    if not weather:
      raise Http404
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)

class WeatherSpecificDate(APIView):
  '''
  Returns the measurements of the weather_station_id for the date = YYYY-MM-DD
  url: http://127.0.0.1:8000/weather_station/<ID>/<year>/<month>/<day>
  '''
  def get(self, request, weather_station_id, year, month, day):
    dateObject = datetime.datetime(year=int(year), month=int(month), day=int(day))
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather = weather.filter(date=dateObject)
    if not weather:
      raise Http404
    serializer = WeatherSerializer(weather, many=True)
    return Js(serializer.data)

class Valve(APIView):
  '''
  Android App posts ID and desired valve_status. The server saves the valve_status in the Valve database table
  and waits a request from the TCP script which gets the valve status from there and if different than the previous 
  valve's status sends the new value to the weather station
  POST url: http://127.0.0.1:8000/weather_station/valve

  GET -- Returns only the valve status (if a valid ID is given)
  url: http://127.0.0.1:8000/weather_station/valve/<ID>
  '''
  def get(self, request, weather_station_id):
    try:
      valve = ValveModel.objects.get(ID=weather_station_id)
      response = JsonResponse({'valve_status': valve.valve_status})
      return response
    except:
      raise Http404

  def post(self, request, format=None):
    try:
      vs = request.POST["valve_status"]
      weather_station_id = request.POST["ID"]
      try:
        valve = ValveModel.objects.get(ID=weather_station_id)
        valve.valve_status = vs
        valve.save()
      except:
        raise Http404
    except:
      raise HTTP_400_BAD_REQUEST
    return Response(status=status.HTTP_200_OK)






    









    
