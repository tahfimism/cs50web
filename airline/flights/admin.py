from django.contrib import admin
from .models import Airport, Flight, Passenger

# Register your models here.

# add custom configirations for adminmodel to make it more cool
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")
    list_filter = ("origin", "destination")
    search_fields = ("origin__city", "destination__city")

# generate adminmodel config for  passenger
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
    
admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
