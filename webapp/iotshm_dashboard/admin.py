# Register your models here.
from django.contrib import admin
from iotshm_dashboard.models import Building,Sensor

class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','number', 'manager']}),
        ('Location',         {'fields': ['address', 'city', 'state', 'zipcode']}),
    ]
    list_display = ('name','number', 'manager','address', 'city', 'state', 'zipcode')
    list_filter = ['number','manager', 'name']
    search_fields = ['number','manager']

class SensorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['building','id']}),
    ]
    list_display = ('building','id')
    list_filter = ['building','id']

admin.site.register(Building,BuildingAdmin)
admin.site.register(Sensor,SensorAdmin)