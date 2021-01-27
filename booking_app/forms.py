from django import forms

from django.contrib.auth import forms as authform 
from django.contrib.auth import (
    authenticate,
    get_user_model
) 
from django.contrib.admin import widgets
import datetime
User = get_user_model()
DATE_INPUT_FORMATS = ['%d-%m-%Y']
from .models import Floor,Seat, SeatBooking

def check_size(value):
  if len(value) < 6:
    raise forms.ValidationError("the Password is too short")


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
  
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user_qs = User.objects.filter(username=username)
            if not user_qs.exists():
                print("i am here")
                raise forms.ValidationError("User does not exist") 
            if not authenticate(username = username, password = password):
                raise forms.ValidationError("incorect password") 
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators = [check_size])
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label ='Email Address')
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]
    
    def clean_email(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        if password != password2:
            raise forms.ValidationError("Passwords must match",code='invalid')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email already registered",code='invalid')
        return email
        #return super(UserRegisterForm, self).clean(*args, **kwargs)  

class BookingDateForm(forms.Form):
    #booking_date = forms.DateField()
    booking_date = forms.DateField()

    #booking_date = forms.DateField(auto_now=True,label='Booking Date', widget=forms.SelectDateWidget(input_formats= DATE_INPUT_FORMATS))
    def clean_booking_date(self, *args, **kwargs):
        booking_date = self.cleaned_data.get('booking_date')
        ##password = self.cleaned_data.get('password')

        if booking_date:
            #user_qs = User.objects.filter(username=username)
            if booking_date < datetime.date.today():
                print("i am here")
                raise forms.ValidationError("Seat Booking of past date not allowed!!!") 
            elif booking_date > datetime.date.today()  + datetime.timedelta(days=7):
                raise forms.ValidationError("Seat Booking of allowed only of 1 week in advance (5 working days) !!!")
        return super(BookingDateForm, self).clean(*args, **kwargs)  
        
class CancelBookingForm(forms.Form):
    #booking_date = forms.DateField()
    #booking_date = forms.DateField()
    #id = forms.IntegerField()

    #booking_date = forms.DateField(auto_now=True,label='Booking Date', widget=forms.SelectDateWidget(input_formats= DATE_INPUT_FORMATS))
    def clean(self, *args, **kwargs):
        # booking_date = self.cleaned_data.get('booking_date')
        # ##password = self.cleaned_data.get('password')
        # print("booking date got in cancel form="+booking_date)
        # if booking_date:
        #     #user_qs = User.objects.filter(username=username)
        #     if booking_date < datetime.date.today():
        #         print("i am here")
        #         raise forms.ValidationError("Cancel Booking of past date not allowed!!!") 
        #     elif booking_date > datetime.date.today()  + datetime.timedelta(days=7):
        #         raise forms.ValidationError("Cancelation Booking of allowed only of 1 week in advance (5 working days) !!!")
        return super(CancelBookingForm, self).clean(*args, **kwargs) 


class SelectFloorShiftForm(forms.Form):
    floor = forms.IntegerField()
    shift = forms.CharField()
    booking_date = forms.DateField()
    def clean(self, *args, **kwargs):
        floor = self.cleaned_data.get('floor')
        shift = self.cleaned_data.get('shift')
        booking_date = self.cleaned_data.get('booking_date')
        if floor < 0:
            raise forms.ValidationError("Wrong Floor") 
        return super(SelectFloorShiftForm, self).clean(*args, **kwargs)   



class BookSeatForm(forms.Form):
    floor = forms.IntegerField()
    shift = forms.CharField()
    booking_date = forms.DateField()
    booked_by = forms.CharField()
    seat_row = forms.CharField()
    seat_num = forms.IntegerField()
    seat_id = forms.IntegerField()
    def clean(self, *args, **kwargs):
        floor = self.cleaned_data.get('floor')
        shift = self.cleaned_data.get('shift')
        booking_date = self.cleaned_data.get('booking_date')
        #TODO more validations but later, like already booked
        if floor < 0:
            raise forms.ValidationError("Wrong Floor") 
        return super(BookSeatForm, self).clean(*args, **kwargs)   

class AddFloorForm(forms.ModelForm):
    floor_num = forms.IntegerField()
    class Meta:  
        model = Floor  
        fields = "__all__"
    def clean(self, *args, **kwargs):
        floor_num = self.cleaned_data.get('floor_num')
        if floor_num:
            all_floors_with_num = Floor.objects.filter(floor_num= floor_num)
            floors_with_num = []
            for f in all_floors_with_num:
                if int(f.floor_num) == floor_num:
                    floors_with_num.append(floor_num)           
                if floor_num < 0:
                    raise forms.ValidationError("No negative floor allowed")
                elif floor_num in floors_with_num:
                    raise forms.ValidationError("Floor "+str(floor_num)+" already exists")
                    
        return super(AddFloorForm, self).clean(*args, **kwargs)  

class AddSeatForm(forms.ModelForm):
    floor = forms.IntegerField()
    row = forms.CharField(max_length=10)
    seat_num = forms.IntegerField() 
    class Meta:  
        model = Seat  
        fields = "__all__"
    def clean(self, *args, **kwargs):
        floor = self.cleaned_data.get('floor')
        row = self.cleaned_data.get('row')
        seat_num = self.cleaned_data.get('seat_num')

        if floor and row and seat_num:
            floor_qs = Floor.objects.filter(floor_num=floor)
            if floor < 0 or seat_num < 0:
                print("i am here")
                raise forms.ValidationError("No neggatives please")
            if not floor_qs.exists():
                raise forms.ValidationError("Floor doesnt exist")
            else:
                seat_qs = Seat.objects.filter(floor=floor, row=row,seat_num =seat_num)
                if seat_qs.exists():
                    raise forms.ValidationError("Seat already exists")
        else:
            raise forms.ValidationError("Fill all fields") 
        return super(AddSeatForm, self).clean(*args, **kwargs)  