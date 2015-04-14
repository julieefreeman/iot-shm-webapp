from django.db import models
from localflavor.us.models import USStateField
from django.contrib.auth.models import User

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

class SensorRDS(models.Model): # in RDS database - not locally stored
    building_id = models.IntegerField()
    id = models.CharField(max_length=300, primary_key=True)  # AutoField?

    class Meta:
        managed = False
        db_table = 'Sensor'

    def __str__(self):
        return "#%s (%d)" % (self.id, self.building_id)

# class MagnitudeRDS1(models.Model): # in RDS database - not locally stored
#     sensor_id = models.CharField(max_length=300,primary_key=True) #foreign key due to the way it's coded
#     timestamp = models.DateTimeField(primary_key=True)
#     magnitude = models.FloatField()
#     reading_type = models.IntegerField(primary_key=True)
#     healthy = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'Magnitude'

class MagnitudeRDS2(models.Model): # in RDS database - not locally stored
    sensor_id = models.CharField(max_length=300,primary_key=True) #foreign key due to the way it's coded
    timestamp = models.DateTimeField(primary_key=True)
    magnitude = models.FloatField()
    reading_type = models.IntegerField(primary_key=True)
    healthy = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'MagnitudeV2'