from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import pandas as pd
from .models import Courses
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
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

        if (len(username)>6):
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
            request.session['last_name'] = last_name
            request.session['adm_no'] = adm_no
            request.session.set_expiry=3600


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


def check_sessions(request):
    if request.user.is_authenticated:
        fname=request.session['first_name']
        return render(request,"authentication/career_choice.html",{'fname':fname})
    else:
        messages.error(request,'Please log in to the system')
        return redirect('homepage')

def check_marks(request):
    if request.method == 'POST':
        mathematics = request.POST['maths']
        maths=int(mathematics)

        english = request.POST['eng']
        eng=int(english)

        kiswahili = request.POST['kisw']
        kisw =int(kiswahili)

        biology =request.POST['bio']
        bio=int(biology)

        chemistry =request.POST['chem']
        chem=int(chemistry)

        physics =request.POST['phy']
        phy=int(physics)

        bussiness = request.POST['bied']
        bied=int(bussiness)

        geography =request.POST['geo']
        geo=int(geography)

        history =request.POST['histo']
        histo=int(history)

        religion_studies =request.POST['religion']
        religion=int(religion_studies)

        music_studies = request.POST['music']
        music=int(music_studies)

        agric_studies = request.POST['agric']
        agric=int(agric_studies)

        comp_studies = request.POST['comp']
        comp=int(comp_studies)

        home_sci_studies =request.POST['home_sci']
        home_sci=int(home_sci_studies)

        all_subjects={'Subject':['MAT','ENG','KIS','BIO','CHEM','PHY','BIED','GEO','HIS','REL','MUS','AGR','COM','HOM'],
                            'Marks':[maths,eng,kisw,bio,chem,phy,bied,geo,histo,religion,music,agric,comp,home_sci]}
        df=pd.DataFrame(all_subjects)

        for index,rows in df.iterrows():
            if rows[1] > 0:
                sum=df['Marks'].sum(axis=0)
                average = sum/8
                common_string="You got an "
                if average < 27:
                    mark="E"
                    grade=common_string +mark
                if average <= 32 and average >= 27:
                    mark="D-"
                    grade=common_string + mark
                if average <= 37 and average >= 33:
                    mark="D"
                    grade=common_string +mark
                if average <= 42 and average >= 38:
                    mark="D+"
                    grade=common_string + mark
                if average <= 47 and average >= 43:
                    mark="C-"
                    grade=common_string + mark
                if average <= 52 and average >= 48:
                    mark="C"
                    grade=common_string +mark
                if average <= 57 and average >= 53:
                    mark="C+"
                    grade=common_string + mark
                if average <= 62 and average >= 58:
                    mark="B-"
                    grade=common_string + mark
                if average <= 67 and average >= 63:
                    mark="B"
                    grade=common_string +mark
                if average <= 72 and average >= 68:
                    mark="B+"
                    grade=common_string + mark
                if average <= 77 and average >= 73:
                    mark="A-"
                    grade=common_string + mark
                if average <= 78 and average >= 100:
                    mark="A"
                    grade=common_string +mark
                elligible_course=Courses.objects.get(acceptable_grade=mark)
                elligible_course_name=elligible_course.title
                elligible_course_desc=elligible_course.short_description

        return render(request,"authentication/career_marks.html",{'average':average,'grade':grade,'e_cn':elligible_course_name,'e_cd':elligible_course_desc})