from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound  
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Floor,Seat, SeatBooking
#importing loading from django template  
from django.template import loader
import datetime
from .utils import rev_date, send_cancellation_mail, is_user_admin
from .dao import get_first_half_seats, get_second_half_seats, get_seat_bookings_for_user
from seat_booking import settings
from django.core.mail import send_mail 
from .form import CreateUserForm
from .forms import (UserLoginForm, UserRegisterForm, 
BookingDateForm, BookSeatForm, AddFloorForm, 
AddSeatForm, SelectFloorShiftForm, CancelBookingForm)

def register_view(request, *args, **kwargs):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username =username, password = password)
            login(request, user)
            if next:
                redirect(next)
            return redirect('/home')
        else: 
            context = {
                'form':form
            }
            return render(request, "register.html", context)            

    context = {
        'form':form
    }
    return render(request, "register.html", context)


def login_view(request, *args, ** kwargs):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("was here")
            #user = form.save(commit = False)
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username =username, password = password)
            if user is not None:
                login(request, user)
                if next:
                    redirect(next)
                return redirect('/home')
        else:
            print("gotchaaaa")
            #messages.warning(request, "login falied")
            #args['form'] = form #instead of PasswdForm()
            context = {
            'form' : form
            }    
            return render(request, 'login.html', context)

    context = {
        'form' : form
    }
    return render(request, "login.html", context)

@login_required(login_url='login')
def booking_date_form(request, *args, ** kwargs):
    print("got here1")
    is_admin = is_user_admin(request.user.email)
    next = request.GET.get('next')
    form = BookingDateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("was here in booking date")
            booking_date = request.POST.get('booking_date')
            print("booking date was"+ booking_date)
            all_seats = Seat.objects.all()
            all_floors = Floor.objects.all()
            context = {
            #'form' : form,
            'all_seats' :  all_seats,
            'all_floors' : all_floors,
            'is_admin' : is_admin
            }
            #messages.error(request, 'Floor added successfully!')
            return render(request, 'select_floor_n_shift.html', {'all_seats' :  all_seats, 'all_floors' : all_floors, 
            'date': booking_date, 'is_admin' : is_admin})
        else:
            booking_date = request.POST.get('booking_date')
            print("booking date was======"+ booking_date)

            print("gotchaaaa")
            context = {
            'form' : form,
            'is_admin' : is_admin
            }    
            return render(request, 'booking_date_form.html', context)

    context = {
        'form' : form,
        'is_admin' : is_admin
    }
    return render(request, "booking_date_form.html", context)

@login_required(login_url='login')
def select_floor_shift(request, *args, ** kwargs):
    is_admin = is_user_admin(request.user.email)
    print("got here1")
    next = request.GET.get('next')
    form = SelectFloorShiftForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("was here in booking date")
            booking_date = request.POST.get('booking_date')
            floor = request.POST.get('floor')
            shift = request.POST.get('shift')
            print("booking date was "+ booking_date)
            print("floor was "+floor)
            print("shift was "+ shift)

            #TODO move seat fetching to a dao function
            all_seats = Seat.objects.filter(floor =floor)
            all_seats_a_1 = []
            all_seats_a_2 = []
            all_seats_b_1 = []
            all_seats_b_2 = []
            all_seats_c_1= []
            all_seats_c_2 = []
            all_seats_a_1 = get_first_half_seats(floor, 'A')
            all_seats_a_2 = get_second_half_seats(floor, 'A')

            all_seats_b_1 = get_first_half_seats(floor, 'B')
            all_seats_b_2 = get_second_half_seats(floor, 'B')

            all_seats_c_1 = get_first_half_seats(floor, 'C')
            all_seats_c_2 = get_second_half_seats(floor, 'C')                        
            

            all_floors = Floor.objects.all()
            
            r = rev_date(booking_date)
            print("r was")
            print(r)
            all_bookings_of_date = SeatBooking.objects.filter(booking_date = r,shift = shift).order_by('seat_num')
            self_booked_ids = []
            booked_seat_ids = []
            for b in all_bookings_of_date:
                booked_seat_ids.append(b.seat_id)
                if b.booked_by == request.user.username:
                    self_booked_ids.append(b.seat_id)


            print(" filtered seats were")
            print(booked_seat_ids)
            if 1 in booked_seat_ids:
                print("okay")
            context = {
            'all_seats' :  all_seats,
            'all_floors' : all_floors,
            'floor': floor,
            'shift' : shift,
            'booking_date' :booking_date,
            'shift' :shift,
            'self_booked_ids' :self_booked_ids,
            'booked_seat_ids' : booked_seat_ids,
            'all_seats_a_1' : all_seats_a_1,
            'all_seats_b_1' : all_seats_b_1,
            'all_seats_c_1' : all_seats_c_1,
            'all_seats_a_2' : all_seats_a_2,
            'all_seats_b_2' : all_seats_b_2,
            'all_seats_c_2' : all_seats_c_2,
            'is_admin' : is_admin
            }
            print("we did got here")
            #messages.error(request, 'Floor added successfully!')
            return render(request, 'view_seats.html',context)
        else:
            print("gotchaaaa")
            context = {
            'form' : form,
            'is_admin' : is_admin
            }    
            return render(request, 'select_floor_n_shift.html', context)

    context = {
        'form' : form,
        'is_admin' : is_admin
    }
    return render(request, "select_floor_n_shift.html", context)

#BookSeatForm
@login_required(login_url='login')
def book_seat(request, *args, ** kwargs):
    is_admin = is_user_admin(request.user.email)
    print("got here1")
    next = request.GET.get('next')
    form = BookSeatForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            booking_date = request.POST.get('booking_date')
            floor = request.POST.get('floor')
            shift = request.POST.get('shift')
            seat_id = request.POST.get('seat_id')
            seat_row = request.POST.get('seat_row')
            seat_num =request.POST.get('seat_num')
            all_seats = Seat.objects.filter(floor=floor)
            all_seats_a_1 = []
            all_seats_a_2 = []
            all_seats_b_1 = []
            all_seats_b_2 = []
            all_seats_c_1= []
            all_seats_c_2 = []
            all_seats_a_1 = get_first_half_seats(floor, 'A')
            all_seats_a_2 = get_second_half_seats(floor, 'A')

            all_seats_b_1 = get_first_half_seats(floor, 'B')
            all_seats_b_2 = get_second_half_seats(floor, 'B')

            all_seats_c_1 = get_first_half_seats(floor, 'C')
            all_seats_c_2 = get_second_half_seats(floor, 'C')                
            all_floors = Floor.objects.all()
            r = rev_date(booking_date)
            print("in book seat valid form")

            all_bookings_of_date = SeatBooking.objects.filter(booking_date = r,shift = shift)
            booked_seat_ids = []
            prev_self_booked_ids =[]
            for b in all_bookings_of_date:
                booked_seat_ids.append(b.seat_id)
                if b.booked_by == request.user.username:
                    prev_self_booked_ids.append(b.seat_id)
            print("booked seat ids are ")
            print(booked_seat_ids)
            print("seat_id got was"+seat_id)
            booking_possible = False
            if  int(seat_id) in prev_self_booked_ids:
                messages.error(request, "You have already boooked this seat!!!!")
            elif prev_self_booked_ids !=[]:
                messages.error(request, "You have already booked a seat for date "+booking_date+" !!!")
            elif shift =='A' and int(seat_id)%2 ==1:
                messages.error(request,"Only even seat numbers booking allowed for shift A")
            elif shift =='B' and int(seat_id)%2 ==0:
                messages.error(request,"Only odd seat numbers booking allowed for shift B")
            elif int(seat_id) not in booked_seat_ids:
                print("no booking found for seat, will book it")
                sb = SeatBooking.objects.create(booking_date = r,shift = shift, seat_id = seat_id,booked_by = request.user.username,
                seat_row= seat_row, seat_num =seat_num, floor = floor)
                msg = "Hi " + request.user.username +"!!!, your Seat is booked for Seat: "+ seat_row+"-"+str(seat_num) + " Floor" + str(floor)
                #send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
                send_mail("SeatBooking Confirm-SeatBookingApp", msg,settings.EMAIL_HOST_USER,[request.user.email])
                print(sb)
                messages.error(request, "Seat successfully booked for Seat: "+ seat_row+"-"+
                str(seat_num) + " Floor " + str(floor) +" for date: "+booking_date +" shift "+shift+", confirmation mail sent please check inbox")
                booking_possible = True
            else:
                messages.error(request, "Seat already booked!!!!")
                print("already booking found for "+str(seat_id))

            updated_all_bookings_of_date = SeatBooking.objects.filter(booking_date = r,shift = shift)
            booked_seat_ids = []
            self_booked_ids = []
            for b in updated_all_bookings_of_date:
                booked_seat_ids.append(b.seat_id)
                if b.booked_by == request.user.username:
                    self_booked_ids.append(b.seat_id)

            context = {
            'all_seats' :  all_seats,
            'all_floors' : all_floors,
            'floor': floor,
            'booking_date' :booking_date,
            'shift' :shift,
            'booked_seat_ids' : booked_seat_ids,
            'self_booked_ids' : self_booked_ids,
            'all_seats_a_1' : all_seats_a_1,
            'all_seats_b_1' : all_seats_b_1,
            'all_seats_c_1' : all_seats_c_1,
            'all_seats_a_2' : all_seats_a_2,
            'all_seats_b_2' : all_seats_b_2,
            'all_seats_c_2' : all_seats_c_2,
            'is_admin' : is_admin
            }
            print("we did got here")
            #messages.error(request, 'Floor added successfully!')
            return render(request, 'view_seats.html',context)
        else:
            print("gotchaaaa------")
            context = {
            'form' : form,
            'is_admin' : is_admin
            }    
            return render(request, 'select_floor_n_shift.html', context)

    context = {
        'form' : form,
        'is_admin' : is_admin
    }
    return render(request, "select_floor_n_shift.html", context)

@login_required(login_url='login')
def cancel_booking(request, *args, ** kwargs):
    is_admin = is_user_admin(request.user.email)
    print("got in cancel booking")
    next = request.GET.get('next')
    form = CancelBookingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            booking_id = request.POST.get('id')
            print("booking id got was "+booking_id)
            #booking = SeatBooking.objects.filter(id =int(booking_id))
            #print(booking)
            b = SeatBooking.objects.get(id=int(booking_id))  
            print(b)
            msg = ""
            if b.booking_date < datetime.date.today():
                msg = "Booking of past date cannot be cancelled"
            elif b.booking_date < datetime.date.today()  + datetime.timedelta(days=2):
                msg = "Bookings can be cancelled only before 2 days before date of booking"
            elif b.booking_date > datetime.date.today()  + datetime.timedelta(days=7):
                msg = "Bookings of only next 7 days after today can be cancelled "
            else:
                b.delete()
                msg = "Booking sucessfully cancelled for Seat "+b.seat_row+"-"+ str(b.seat_num)+ " for date "+str(b.booking_date)
                send_cancellation_mail(b.booking_date, b.floor, b.seat_row, b.seat_num, b.shift, request.user.email, request.user.first_name)

            messages.error(request, msg)
            bookings_for_user = get_seat_bookings_for_user(request.user.username)
            context = {
                'bookings' : bookings_for_user,
                'is_admin' : is_admin
            }
            print("we did got here")
            #messages.error(request, 'Floor added successfully!')
            return render(request, 'cancel_booking_page.html',context)
        else:
            print("cancel booking form invalid")
            context = {
            'form' : form,
            'is_admin' : is_admin
            }    
            return render(request, 'cancel_booking_page.html', context)

    context = {
        'form' : form,
        'is_admin' : is_admin
    }
    return render(request, "cancel_booking_page.html", context)

def cancel_booking_page(request, *args, ** kwargs):
    is_admin = is_user_admin(request.user.email)
    bookings_for_user = get_seat_bookings_for_user(request.user.username)
    seat_ids = []
    for b in bookings_for_user:
        print(b.seat_num)
        seat_ids.append(b.seat_num)
    bookings = []
    if seat_ids == []:
        print("no bookings found")
        messages.error(request, 'You have no seat booked')
        bookings = []
    else:
        print("bookings found")
        bookings = bookings_for_user
    
    context = {
        'bookings' : bookings_for_user,
        'is_admin' : is_admin
    }

    return render(request, 'cancel_booking_page.html', context)    


def add_floor(request, *args, ** kwargs):
    is_admin = is_user_admin(request.user.email)
    print("testing config ="+settings.TEST_CONFIG)
    print("got here1")
    next = request.GET.get('next')
    form = AddFloorForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("was here in floor")
            form.save()
            #user = form.save(commit = False)
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            context = {
            'form' : form,
            'msg' : "Floor added Sucessfully",
            'is_admin' : is_admin
            }
            messages.error(request, 'Floor added successfully!')
            render(request, 'add_floor.html', context)
        else:
            floor_num = request.POST.get('floor_num')
            print("  "+floor_num)
            print("gotchaaaa")
            #messages.warning(request, "login falied")
            #args['form'] = form #instead of PasswdForm()
            context = {
            'form' : form,
            'is_admin' : is_admin
            }    
            return render(request, 'add_floor.html', context)

    context = {
        'form' : form,
        'is_admin' : is_admin
    }
    return render(request, "add_floor.html", context)

def add_seat(request, *args, ** kwargs):
    is_admin = is_user_admin(request.user.email)
    print("got here1")
    next = request.GET.get('next')
    form = AddSeatForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("was here in seat")
            form.save()
            #user = form.save(commit = False)
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            context = {
            'form' : form,
            'is_admin' : is_admin
            }
            messages.error(request, 'Seat added successfully!')
            return render(request, 'add_floor.html', context)
        else:
            print("gotchaaaa")
            context = {
            'form' : form,
            'is_admin' : is_admin
            }    
            return render(request, 'add_floor.html', context)

    context = {
        'form' : form,
        'is_admin' : is_admin
    }
    return render(request, "add_floor.html", context)


@login_required(login_url='login')
def home(request, *args, **kwargs):
    is_admin = is_user_admin(request.user.email)
    print("user name is already set as "+request.user.username)
    return render(request, 'home.html', {'is_admin' : is_admin})


def logout_view(request):
    logout(request)
    return render(request, "index.html")

#below are older tries
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data.get('password1')
                print("password1 was"+ password1)
                password2 = form.cleaned_data.get('password2')
                if password1 != password2:
                    raise forms.validationError("Passoword dont match")
                form.save()
                user = form.cleaned_data.get('username')
        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home/")
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def index(request):  
   template = loader.get_template('index.html')
   name =  {'test' : 'test'}
   return HttpResponse(template.render(name)) 
       
def mail(request):  
    subject = "Greetings"  
    msg     = "Testing django mail"  
    to      = "xyz@gmail.com"  
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfuly"  
    else:  
        msg = "Mail could not sent"  
    return HttpResponse(msg)  
