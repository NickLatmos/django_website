from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weather as WeatherModel, Valve as ValveModel, WeatherStation as WeatherStationModel
from .serializer import WeatherSerializer, WeatherStationSerializer
import datetime
import logging, json

logger = logging.getLogger(__name__)

class WeatherStation(APIView):
    # GET method -- Used for ID validation 
  def get(self, request, weather_station_id):
    try: 
      weather = WeatherStationModel.objects.filter(weather_station_id=weather_station_id)
      if not weather:
        raise Http404
      return Response(status=status.HTTP_200_OK)
    except WeatherStationModel.DoesNotExist:
      raise Http404
      
class Weather(APIView):
  '''
  Return all the weather measurements for the specified weather station
  Posts new weather data from the specified weather station (if valid)
  GET url: http://127.0.0.1:8000/weather_station/<ID>
  POST url http://127.0.0.1:8000/weather_station/
  '''

  # GET method -- Used for ID validation 
  def get(self, request, weather_station_id):
    try: 
      weather = WeatherModel.objects.filter(ID=weather_station_id)
      if not weather:
        raise Http404
      #serializer = WeatherSerializer(weather, many=True)          # When using filter() we must include many=True
      #return Response(serializer.data)
      return Response(status=status.HTTP_200_OK)
    except WeatherModel.DoesNotExist:
      raise Http404

  def post(self, request, format=None):
    logger.warn("request body: %s", request.body)
    serializer = WeatherSerializer(data=request.data)
    # If the posted weather station's ID is not equal to anyone from the database then reject it.
    if serializer.is_valid():
      serializer.save()
      logger.warn('Successfully posted data:\n %s', json.dumps(request.POST, indent=4, sort_keys=True))
      self.pretty_request(request, logger)
      return (Response('{Data successfully posted}', status=status.HTTP_201_CREATED))
    self.pretty_request(request, logger)
    logger.warn('Here is the post data:\n %s', json.dumps(request.POST, indent=4, sort_keys=True))
    return (Response('{Something went wrong}', status=status.HTTP_400_BAD_REQUEST))
  
  def pretty_request(self, request, logger):
    content_length = request.META["CONTENT_LENGTH"] 
    host = request.META["HTTP_HOST"]
    content_type = request.META["CONTENT_TYPE"]
    port = request.META["SERVER_PORT"]
    logger.warn("CONTENT_LENGTH: %s", content_length)
    logger.warn("HTTP_HOST: %s", host)
    logger.warn("SERVER_PORT: %s", port)
    logger.warn("CONTENT_TYPE: %s", content_type)
     
class WeatherToday(APIView):
  '''
  Returns the last weather measurement for the specified weather station
  url: http://127.0.0.1:8000/weather_station/today/<ID>
  '''
  def get(self, request, weather_station_id):
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather = weather.filter(date=datetime.date.today())
    if not weather:
      raise Http404
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)

class WeatherLastMeasurement(APIView):
  '''
  Returns the weather measurements in the last <days> days
  url: http://127.0.0.1:8000/weather_station/last_measurement/<ID>/
  '''
  def get(self, request, weather_station_id):
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather1 = weather.order_by('-date','-time')[0]
    if not weather1:
      raise Http404
    serializer = WeatherSerializer(weather1, many=False)
    return Response(serializer.data)

class WeatherLastMeasurements(APIView):
  '''
  Returns the weather measurements for the month <month> (in decimal represantation)
  url: http://127.0.0.1:8000/weather_station/<ID>/last_measurements/<max_number>/interval/<interval>/
  '''
  def get(self, request, weather_station_id, max_number, interval):
    try:
      weather = WeatherModel.objects.filter(ID=weather_station_id)
      if int(interval) <= 20:
        date_threshold = datetime.datetime.now() - datetime.timedelta(days=1)
      elif int(interval) <= 40 and int(max_number) <= 30:
        date_threshold = datetime.datetime.now() - datetime.timedelta(days=2)
      else:
        time_threshold = datetime.datetime.now() - datetime.timedelta(days=3)
      weather = weather.objects.filter(date__gte=date_threshold)
      if not weather:
        raise Http404
      serializer = WeatherSerializer(weather, many=True)
      return Response(serializer.data)
    except WeatherModel.DoesNotExist:
      raise Http404

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
    return Response(serializer.data)

class WeatherDateTimeRange(APIView):
  '''
  Returns the measurements of the weather_station_id from a specific date
  and time to a specific date and time.
  url: http://127.0.0.1:8000/weather_station/<ID>/from/<year>/<month>/<day>/<hour>/<minute>/<seconds>
  /to/<year>/<month>/<day>/<hour>/<minute>/<seconds>/
  '''
  def get(self, request, weather_station_id, year_from, month_from, day_from, hour_from, minute_from, second_from,
          year_to, month_to, day_to, hour_to, minute_to, second_to):
    dateObjectFrom = datetime.datetime(year=int(year_from), month=int(month_from), day=int(day_from))
    timeObjectFrom = datetime.time(hour=int(hour_from), minute=int(minute_from), second=int(second_from))
    dateObjectTo = datetime.datetime(year=int(year_to), month=int(month_to), day=int(day_to))
    timeObjectTo = datetime.time(hour=int(hour_to), minute=int(minute_to), second=int(second_to))
    weather = WeatherModel.objects.filter(ID=weather_station_id)
    weather = weather.filter(date__gte=dateObjectFrom)
    #weather = weather.exclude(date=dateObjectFrom, time__lte=timeObjectFrom)
    weather = weather.filter(date__lte=dateObjectTo)
    #weather = weather.exclude(date=dateObjectTo, time__gte=timeObjectTo)
    weather = weather.filter(time__gte=timeObjectFrom, time__lte=timeObjectTo)
    if not weather:
      raise Http404
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)

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
      raise Http404
    return Response(status=status.HTTP_200_OK)






    









    
