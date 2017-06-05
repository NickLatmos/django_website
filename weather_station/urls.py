from django.conf.urls import url
from . import views

urlpatterns = [
  
  # For post() method -- Weather measurements
  # http://192.168.1.60:5000/weather_station/ the data (+ID) are in the payload
  url(r'^$', views.Weather.as_view()),     
  # For post() method -- Valve status -- Needs ID and valve_status in the payload
  url(r'^valve/$', views.Valve.as_view()),

  # /weather_station/valve/<ID>
  url(r'^valve/(?P<weather_station_id>[\w]+)/$', views.Valve.as_view()),
  # The weather station ID can be any alphanumeric character
  url(r'^validate/(?P<weather_station_id>[\w]+)/$', views.WeatherStation.as_view()),
  # url: /weather_station/today/<ID>
  url(r'^today/(?P<weather_station_id>[\w]+)/$', views.WeatherToday.as_view()),
  # url: /weather_station/XYZ/days/20
  url(r'^(?P<weather_station_id>[\w]+)/days/(?P<days>[0-9]{1,3})/$', views.WeatherLastDays.as_view()),
  # url: /weather_station/XYZ/month/04
  url(r'^(?P<weather_station_id>[\w]+)/month/(?P<month>[0-9]{2})/$', views.WeatherSpecificMonth.as_view()),
  # url: /weather_station/XYZ/2017/04/06
  url(r'^(?P<weather_station_id>[\w]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.WeatherSpecificDate.as_view()),
]
