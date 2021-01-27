"""seat_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from booking_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('index/', views.index),
    path('mail',views.mail),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('add-floor/',views.add_floor),
    path('add-seat/',views.add_seat),
    path('select_date/',views.booking_date_form),
    path('select_floor_shift', views.select_floor_shift),
    path('book_seat', views.book_seat),
    path('cancel_booking_page', views.cancel_booking_page),
    path('cancel_booking', views.cancel_booking),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html',
            success_url='/login'
        ),
        name='change-password'
    ),    
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password_reset.html',
             subject_template_name='common/password_reset_subject.txt',
             email_template_name='common/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password_reset_complete.html'
         ),
         name='password_reset_complete')

    #path('register/', views.registerPage, name="register"),
    # path('login/', views.loginPage, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
    # path('home/', views.home, name="home"),
]

