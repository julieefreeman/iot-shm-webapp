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
        return "%s (%d)" % (self.address, self.number)