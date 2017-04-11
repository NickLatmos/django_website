from django.contrib import admin
from .models import WeatherStation, Weather, Valve

# Register your models here.
admin.site.register(WeatherStation)
admin.site.register(Weather)
admin.site.register(Valve)