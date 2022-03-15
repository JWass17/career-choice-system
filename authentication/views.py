from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render


#Redirection to homepage
def homepage(request):
    return render(request,"authentication/homepage.html")
#Authentication methods
#1.Registration method
def reg_user(request):
    if request.method == "POST":
        username=request.POST["username"]
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]

        if (len(username)!=6):
            messages.error(request,'Please enter a valid admission number')
            return redirect('register')
        if User.objects.filter(username=username):
            messages.error(request, "Admission number already exist! Please enter your own admission number.")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered under an account!")
            return redirect('register')
        if pass1!=pass2:
            messages.error(request,"Passwords do not match")
            return redirect('register')
        if not username.isalnum():
            messages.error(request,"Username must be alpha-numeric!")
            return redirect('register')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
        user=User.objects.get(email=email)
        messages.success(request,"Your account has been successfully created!")

         #Welcome Email
         #subject = "Welcome to Soca-Scores"
         #message = "Hello" +" "+ myuser.username + "!! \n" + "Welcome to SocaScores!!\n Thank you for joining the Soca-Scores.This email serves as your confirmation email. Enjoy your time with us. \n\nChairman\nNyambok Julius"
         #from_email = settings.EMAIL_HOST_USER
         #to_list = [myuser.email]
         #send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('login')
    return render(request,"authentication/registration_page.html")

#2 Log In method
def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request,user)
            adm_no=user.username
            first_name=user.first_name
            last_name=user.last_name
            request.session['first_name'] = first_name
            return render(request,"authentication/homepage.html", {'first_name':first_name,'last_name':last_name,'adm_no':adm_no})

        else:
            messages.error(request, "Invalid Credentials entered!")
            return redirect('homepage')
    return render(request,"authentication/login_page.html")

#4 Signing out
def signout(request):
    logout(request)
    messages.success(request,"Signed out successfully")
    return redirect ('homepage')