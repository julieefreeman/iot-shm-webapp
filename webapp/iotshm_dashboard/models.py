from django.db import models
from localflavor.us.models import USStateField
from django.contrib.auth.models import User
from time import strftime, gmtime

class Building(models.Model):
    manager = models.ForeignKey(User)
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = USStateField()
    zipcode = models.IntegerField(max_length=5)
    def __str__(self):
        return "%s (%d)" % (self.name, self.number)

# *************GET RID OF MEEEE*************
# class Sensor(models.Model): # stored in the webapp database
#     building = models.ForeignKey(Building)
#     id = models.IntegerField(primary_key=True)  # AutoField?
#
#     class Meta:
#         managed = True
#         db_table = 'Sensor'
#
#     def __str__(self):
#         return "#%d (%s)" % (self.id, self.building.name)

# class DataPoint(models.Model): # in RDS database - not locally stored
#     id = models.IntegerField(primary_key=True)  # AutoField?
#     sensorid = models.ForeignKey('Sensor', db_column='sensorId')  # Field name made lowercase.
#     value = models.FloatField()
#     healthy = models.CharField(max_length=45)
#
#     class Meta:
#         managed = False
#         db_table = 'Data'
# *************GET RID OF MEEEE*************

class SensorRDS(models.Model): # stored in the remote database
    building_id = models.IntegerField()
    id = models.CharField(max_length=300, primary_key=True)  # AutoField?

    class Meta:
        managed = False
        db_table = 'Sensor'

    def __str__(self):
        return "#%s (%d)" % (self.id, self.building_id)

class HealthScore(models.Model): # in RDS database - not locally stored
    # sensor_id = models.ForeignKey('SensorRDS', db_column='id',primary_key=True)  # Field name made lowercase.
    sensor_id = models.CharField(max_length=300, primary_key=True) #foreign key due to the way it's coded
    timestamp = models.DateTimeField(primary_key=True)
    x_health = models.IntegerField()
    y_health = models.IntegerField()
    z_health = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Health'

    # def __str__(self):
    #     x = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime(self.timestamp))
    #     return "%s (%s)" % (self.sensor_id, x)

class Magnitude(models.Model): # in RDS database - not locally stored
    # sensor_id = models.ForeignKey('SensorRDS', db_column='id')  # Field name made lowercase.
    sensor_id = models.CharField(max_length=300) #foreign key due to the way it's coded
    timestamp = models.DateTimeField()
    x_magnitude = models.FloatField()
    y_magnitude = models.FloatField()
    z_magnitude = models.FloatField()
    frequency = models.FloatField()
    reading_id = models.CharField(max_length=300,primary_key=True)

    class Meta:
        managed = False
        db_table = 'Magnitude'

    # def __str__(self):
    #     x = strftime("%a, %d %b %Y %H:%M:%S +0000", self.timestamp)
    #     return "%s (%s)" % (self.reading_id, x)