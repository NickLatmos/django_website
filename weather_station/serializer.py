"""
The serialzer will return a JSON format for the Stock class members
"""
from rest_framework import serializers
from .models import WeatherStation, Weather, Valve

class WeatherStationSerializer(serializers.ModelSerializer): 
  
  class Meta: 
    # the model we need to serialize
    model = WeatherStation
    # return specific members or everything 
    #fields = ('ticker', 'volume')
    fields = '__all__'

class WeatherSerializer(serializers.ModelSerializer):
  class Meta: 
    # the model we need to serialize
    model = Weather
    # return specific members or everything 
    #fields = ('ticker', 'volume')
    fields = '__all__'
