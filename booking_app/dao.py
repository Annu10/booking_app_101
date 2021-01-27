from .models import Floor,Seat, SeatBooking
import datetime


def get_first_half_seats(floor, row):
    all_seats_a = Seat.objects.filter(floor=floor, row =row).order_by('seat_num')
    i = 0
    all_seats_a_1 = []
    all_seats_a_2 = []
    l = len(all_seats_a)
    while i < l/2:
        all_seats_a_1.append(all_seats_a[i])
        i+=1
    return all_seats_a_1  

def get_second_half_seats(floor, row):
    all_seats_a = Seat.objects.filter(floor=floor, row = row).order_by('seat_num')
    i = 0
    all_seats_a_1 = []
    all_seats_a_2 = []
    l = len(all_seats_a)

    if l %2 ==0:
        i= int(l/2)
    else:
        i = int(l/2) +1
    while i < l:
        all_seats_a_1.append(all_seats_a[i])
        i+=1
    return all_seats_a_1 

def get_seat_bookings_for_user(username):
    d1 = datetime.date.today()
    d2 = datetime.date.today() + datetime.timedelta(days=7)
    print(d2)
    bookings_for_user = SeatBooking.objects.filter(booked_by = username, booking_date__range=[d1, d2]).order_by('booking_date')
    return bookings_for_user