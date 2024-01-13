from django.shortcuts import render, redirect
from app.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import datetime
# Create your views here.
import os
from django.contrib.auth.decorators import login_required

# Create your views here.
def Login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        

        if user:
            login(request, user)
            if user.is_staff:
                return redirect('/admin-panel/index/')           
        else:
            messages.error(request, "Username or password incorrect")
            return redirect('/admin-panel/')   
    else:
        return render(request, "myadmin/page-login.html")


def logout_call(request):
    logout(request)
    return redirect('/admin-panel/')


@login_required(login_url="/admin-panel/")
def DashboardPage(request):
    notify = User.objects.filter(is_user=True, join_by_refer=request.user.refer_code).count()
    # my_user = User.objects.filter(join_by_refer=request.user.refer_code).count
    # num_help = HelpAndSupport.objects.filter(is_completed=False).count()
    # num_withdraw = WithdrawRequest.objects.filter(is_completed=False).count()
    # num_notif = Notification.objects.filter(is_completed=False, read_status=False).count()
    # print("num_notif",num_notif)
    # notification = Notification.objects.filter(is_completed=False, read_status=False)
    
    # ,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif
    return render(request, "myadmin/index.html", {"notify":notify})


@login_required(login_url="/admin-panel/")
def UserTablePage(request):
    get_users = User.objects.filter(is_superuser=False,is_staff=False)
    # filter user which is joined by loggedin user refer code
    my_user = User.objects.filter(join_by_refer=request.user.refer_code)
    
    return render(request, "myadmin/user-table.html", {'my_user':my_user})

@login_required(login_url="/admin-panel/")
def UserCreatePage(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        uname = request.POST["contact"]
        active = request.POST["actv"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        vrfy = request.POST["verificat"]
        above = request.POST["goto"]
        profile = request.FILES['profile_pic']
        pwd = request.POST["password"]
        refer = request.POST["join_by_refer"]
        
        birthdate_obj = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))
        
        print("age>>>>>>", age)
        if age >= 18:       
            if User.objects.filter(mobile_no=contact).exists():
                messages.error(request, 'Contact number already taken')
                return redirect('/admin-panel/new-user/')
            else:
                usr = User(first_name=fname, username=uname, password=make_password(pwd), is_active=active, profile_picture=profile, mobile_no=contact,date_of_birth=dob, gender=gender, is_verified=vrfy,is_above18=above,is_user=True,join_by_refer=refer)
                usr.save()
                return redirect("/admin-panel/users-table/")
        else:
            messages.error(request,"You are not Eligible")
            return redirect('/admin-panel/new-user/')
    else:
        return render(request, "myadmin/create-user.html")
    
        

@login_required(login_url="/admin-panel/")
def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/admin-panel/users-table/")



@login_required(login_url="/admin-panel/")
def DetailUser(request, id):
    get_user = User.objects.get(id=id)
    
    
    return render(request, "myadmin/app-profile.html", {'get_user':get_user})



@login_required(login_url="/admin-panel/")
def EditUser(request, id):
    upleid = User.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST["fname"]
        uname = request.POST["contact"]
        active = request.POST["actv"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        verify = request.POST['verificat']
        yourin = request.POST['goto']
        
        
        if len(request.FILES) !=0:
            if len(upleid.profile_picture) > 0:
                os.remove(upleid.profile_picture.path)
                print(upleid.profile_picture.path)
            upleid.profile_picture = request.FILES['profile_pic']
            
            upleid.save()
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname, username=uname, is_active=active, mobile_no=contact,date_of_birth=dob, gender=gender, is_verified=verify,is_above18=yourin)
        messages.success(request, f"{fname}, profile updated successfully")
        return redirect("/admin-panel/users-table/")
    else:
        getUser = User.objects.get(id=id)    
        return render(request, "myadmin/edituser.html", {'user':getUser})

