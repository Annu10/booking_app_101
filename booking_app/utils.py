from django.core.mail import send_mail 
from django.http import HttpResponse, HttpResponseNotFound  
from seat_booking import settings
import datetime

def rev_date(str):
    print("str to reverse")
    print(str)
    tempstrlist = str.split("-")
    result = tempstrlist[2] + "-"+ tempstrlist[1] +"-" + tempstrlist[0]
    return result

def send_mail_util(to, msg,subject):
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfuly"  
    else:  
        msg = "Mail could not sent"  
    return HttpResponse(msg)

def send_cancellation_mail(booking_date, floor, seat_row, seat_num, shift, to, first_name):
    msg = "Hi "+first_name+", Your Booking for seat : "+seat_row+"-"+ str(seat_num)+ " for date "+str(booking_date)+ " , floor :"+str(floor)+" has been cancelled succesfully"
    subject ="Seat Booking Cancellation"
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfuly"  
    else:  
        msg = "Mail could not sent"  
    return HttpResponse(msg)
