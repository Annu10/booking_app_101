from __future__ import unicode_literals 
from django.db import models


#Create your models here.
DATE_INPUT_FORMATS = ['%d-%m-%Y']
#tables

class Floor(models.Model):  
    floor_num = models.IntegerField()
    class Meta:  
        db_table = "floor"  

class Seat(models.Model):
    floor = models.IntegerField()
    row = models.CharField(max_length=10)
    seat_num = models.IntegerField() 
    class Meta:  
        db_table = "seat"

class SeatBooking(models.Model):
    
    booking_date = models.DateField()
    shift = models.CharField(max_length=10)
    booked_by = models.CharField(max_length=500)
    floor = models.IntegerField()
    seat_row = models.CharField(max_length=10)
    seat_num = models.IntegerField()
    seat_id = models.IntegerField()
    class Meta:
        db_table = "seatbooking"



