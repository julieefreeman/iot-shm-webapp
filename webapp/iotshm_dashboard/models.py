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

class Sensor(models.Model):
    building = models.ForeignKey(Building)
    id = models.IntegerField(primary_key=True)  # AutoField?

    class Meta:
        managed = True
        db_table = 'Sensor'

    def __str__(self):
        return "#%d (%s)" % (self.id, self.building.name)

class DataPoint(models.Model): # in RDS database - not locally stored
    id = models.IntegerField(primary_key=True)  # AutoField?
    sensorid = models.ForeignKey('Sensor', db_column='sensorId')  # Field name made lowercase.
    value = models.FloatField()
    healthy = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Data'