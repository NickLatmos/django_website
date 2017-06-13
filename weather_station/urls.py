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
  # url: /weather_station/last_measurement/XYZ/
  url(r'^last_measurement/(?P<weather_station_id>[\w]+)/$', views.WeatherLastMeasurement.as_view()),
  # url: /weather_station/XYZ/month/04
  url(r'^(?P<weather_station_id>[\w]+)/last_measurements/(?P<max_number>[0-9]{1,3})/interval/(?P<interval>[0-9]{1,3})/$', views.WeatherLastMeasurements.as_view()),
  # url: /weather_station/XYZ/2017/04/06
  url(r'^(?P<weather_station_id>[\w]+)/battery_voltage/$', views.WeatherStationVoltage.as_view()),
  # url: /weather_station/XYZ/2017/04/06
  url(r'^(?P<weather_station_id>[\w]+)/fromdate/(?P<year_from>[0-9]{4})/(?P<month_from>[0-9]{2})/(?P<day_from>[0-9]{2})/todate/(?P<year_to>[0-9]{4})/(?P<month_to>[0-9]{2})/(?P<day_to>[0-9]{2})/fromtime/(?P<hour_from>[0-9]{2})/(?P<minute_from>[0-9]{2})/(?P<second_from>[0-9]{2})/totime/(?P<hour_to>[0-9]{2})/(?P<minute_to>[0-9]{2})/(?P<second_to>[0-9]{2})/$', views.WeatherDateTimeRange.as_view()),
]
