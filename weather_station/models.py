from django.db import models

# Weather Station Model
class WeatherStation(models.Model):
  weather_station_id = models.CharField(primary_key=True, max_length=10)
  owner_name = models.CharField(max_length=40)
  owner_surname = models.CharField(max_length=40)

  def __str__(self):
    return self.weather_station_id + '--' + self.owner_name + '--' + self.owner_surname 

# Weather will have an autoincrement id -- Django currently does not support composite primary keys
class Weather(models.Model):
  '''
  The posted data should have an ID same as the Weather station's primary key otherwise
  a BAD REQUEST 400 will be returned (ID case sensitive).
  Adds automatically the time and date when the object is created
  '''
  ID = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)
  temperature = models.IntegerField()
  humidity = models.IntegerField()
  case_temperature = models.IntegerField()
  pressure = models.BigIntegerField()
  battery = models.DecimalField(max_digits=4, decimal_places=2)
  weather = models.CharField(max_length=30)
  time = models.TimeField(auto_now_add=True, blank=True)
  date = models.DateField(auto_now_add=True, blank=True)

  def __str__(self):
    return ( str(self.ID) + '--' + str(self.temperature) + '--' + str(self.humidity) + '--' 
    + str(self.case_temperature) + '--' + str(self.pressure) + '--' + str(self.weather) + '--' 
    + str(self.date) + '--' + str(self.time))

class Valve(models.Model):
  '''
  Includes the weather station ID with it's user defined valve status
  '''
  ID = models.OneToOneField(WeatherStation, primary_key=True)
  valve_status = models.CharField(max_length=2)

  def __str__(self):
    return (str(self.ID) + ' VALVE ' + str(self.valve_status))
