from django.shortcuts import render, redirect
from app.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import datetime
# Create your views here.
import os
from django.contrib.auth.decorators import login_required
from my_admin.models import *
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


def ProfileInfo(request, id):
    get_data = User.objects.get(id=request.user.id)
    return render(request, "myadmin/profile.html", {"get_data":get_data})


@login_required(login_url="/admin-panel/")
def EditAdminProfile(request, id):
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
        sts = request.POST['state']
        cty = request.POST['city']
        pcd = request.POST['pincode']
        eml = request.POST['email']
        
        if len(request.FILES) !=0:
            if len(upleid.profile_picture) > 0:
                os.remove(upleid.profile_picture.path)
                print(upleid.profile_picture.path)
            upleid.profile_picture = request.FILES['profile_pic']
            
            upleid.save()
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname, username=uname, is_active=active, mobile_no=contact,date_of_birth=dob, gender=gender, is_verified=verify,is_above18=yourin,state_id=sts,city=cty,pincode=pcd,email=eml)
        messages.success(request, f"{fname}, profile updated successfully")
        return redirect(f"/admin-panel/profile/{request.user.id}/")
    else:
        getUser = User.objects.get(id=id) 
        getState = State.objects.all()   
        return render(request, "myadmin/edituser.html", {'user':getUser, 'state':getState})



@login_required(login_url="/admin-panel/")
def DashboardPage(request):
    notify = User.objects.filter(is_user=True, user_admin=request.user.refer_code).count()
    my_user = User.objects.filter(user_admin=request.user.refer_code).count()
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    
    print(num_help)

    return render(request, "myadmin/index.html", {"notify":notify,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})


@login_required(login_url="/admin-panel/")
def UserTablePage(request):
    my_user = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
    # filter user which is joined by loggedin user refer code
    print(request.user.refer_code)
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
                usr = User(first_name=fname, username=uname, password=make_password(pwd), is_active=active, profile_picture=profile, mobile_no=contact,date_of_birth=dob, gender=gender, is_verified=vrfy,is_above18=above,is_user=True,user_admin=request.user.refer_code,join_by_refer=request.user.refer_code)
                usr.save()
                
                random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

                # Create the refer_code using the first 4 characters of the username and the random string
                refcode = usr.username[:4] + random_string
                
                # now new user which we have register by using refer code there user_admin code update new user user_admin field
                uplead = User.objects.filter(id=usr.id)
                uplead.update(refer_code=refcode)
                
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
        sts = request.POST['state']
        cty = request.POST['city']
        pcd = request.POST['pincode']
        eml = request.POST['email']
        
        
        if len(request.FILES) !=0:
            if len(upleid.profile_picture) > 0:
                os.remove(upleid.profile_picture.path)
                print(upleid.profile_picture.path)
            upleid.profile_picture = request.FILES['profile_pic']
            
            upleid.save()
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname, username=uname, is_active=active, mobile_no=contact,date_of_birth=dob, gender=gender, is_verified=verify,is_above18=yourin,state_id=sts,city=cty,pincode=pcd,email=eml)
        messages.success(request, f"{fname}, profile updated successfully")
        return redirect("/admin-panel/users-table/")
    else:
        getUser = User.objects.get(id=id) 
        getState = State.objects.all()   
        return render(request, "myadmin/edituser.html", {'user':getUser, 'state':getState})



@login_required(login_url="/admin-panel/")
def StateCreate(request):
    if request.method == 'POST':
        state = request.POST["cty"]
        if State.objects.filter(name=state).exists():
            messages.info(request, 'State already taken')
            return redirect('/admin-panel/new-state/')
        else:   
            usr = State(name=state)
            usr.save()
            return redirect("/admin-panel/state-table/")
    else:
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-state.html", {'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")
def StateTablePage(request):
    get_state = State.objects.all()
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/state-table.html", {'get_state':get_state,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteState(request, id):
    cty = State.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/state-table/")



@login_required(login_url="/admin-panel/")
def EditState(request, id):
    if request.method == 'POST':
        state = request.POST['cty']     
        if State.objects.filter(name=state).exists():
            messages.info(request, 'State already taken')
            return redirect('/admin-panel/new-state/')
        else:   
            uplead = State.objects.filter(id=id)        
            uplead.update(name=state)
            messages.success(request, f"{state}, State name updated successfully")
            return redirect("/admin-panel/state-table/") 
    else:
        getState = State.objects.get(id=id)   
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-state.html", {'state':getState,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    



@login_required(login_url="/admin-panel/")
def WalletAddCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletamount"]     
        rpoi = request.POST["actv"]      
        
        
        usr = WalletAdd(user_id=gn, walletamount=mfp, walletstatus=rpoi)
        usr.save()
        return redirect("/admin-panel/wallet-add-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-wallet-add.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")   
def WalletAddTablePage(request):
    # Filter walletadd which is objects of currently loggedin user
    get_wallet = WalletAdd.objects.filter(user__user_admin=request.user.refer_code)
    
    
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/wallet-add-table.html", {'get_wallet':get_wallet,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteWalletAdd(request, id):
    cty = WalletAdd.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/wallet-add-table/")


@login_required(login_url="/admin-panel/")
def EditWalletAdd(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletamount"]     
        rpoi = request.POST["actv"]
        
          
        uplead = WalletAdd.objects.filter(id=id)        
        uplead.update(user_id=gn, walletamount=mfp, walletstatus=rpoi)
        messages.success(request, "Wallet add updated successfully")
        return redirect("/admin-panel/wallet-add-table/") 
    else:
        getWallet = WalletAdd.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-wallet-add.html", {'getWallet':getWallet, 'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    
    
@login_required(login_url="/admin-panel/")   
def WalletAmtCreate(request):
    if request.method == 'POST':
        wa = request.POST["walt"]
        gn = request.POST["user"]
        apy_st = request.POST["actv"]
        amt = request.POST["amount"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"]       
        
        
        usr = WalletAmt(walt_id=wa, user_id=gn, payment_status=apy_st, amount=amt,razor_pay_order_id=rpoi,razor_pay_payment_id=tc,razor_pay_payment_signature=sa)
        usr.save()
        return redirect("/admin-panel/wallet-amount-table/")
    else:
        getWallet = WalletAdd.objects.filter(user__user_admin=request.user.refer_code)
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-wallet-amount.html", {'getUser':getUser,'getWallet':getWallet,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")    
def WalletAmtTablePage(request):
    # filter user WalletAmt which is sub-user of currently loggdin user
    get_wallet = WalletAmt.objects.filter(user__user_admin=request.user.refer_code)
    
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/wallet-amount-table.html", {'get_wallet':get_wallet,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DetailWalletAmt(request, id):
    get_wallet = WalletAmt.objects.get(id=id)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/wallet-amount-detail.html", {'get_wallet':get_wallet,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteWalletAmt(request, id):
    cty = WalletAmt.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/wallet-amount-table/")


@login_required(login_url="/admin-panel/")
def EditWalletAmt(request, id):
    if request.method == 'POST':
        wa = request.POST["walt"]
        gn = request.POST["user"]
        apy_st = request.POST["actv"]
        amt = request.POST["amount"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"] 
        
          
        uplead = WalletAmt.objects.filter(id=id)        
        uplead.update(walt_id=wa, user_id=gn, payment_status=apy_st, amount=amt,razor_pay_order_id=rpoi,razor_pay_payment_id=tc,razor_pay_payment_signature=sa)
        messages.success(request, "Wallet amount updated successfully")
        return redirect("/admin-panel/wallet-amount-table/") 
    else:
        getWalletadd = WalletAdd.objects.filter(user__user_admin=request.user.refer_code)
        getWallet = WalletAmt.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-wallet-amount.html", {'getWallet':getWallet, 'getUser':getUser,'getWalletadd':getWalletadd,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    

@login_required(login_url="/admin-panel/")   
def PayByWalletAmountCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletid"]      
        
        
        usr = PayByWalletAmount(user_id=gn, amount=mfp)
        usr.save()
        return redirect("/admin-panel/pay-by-wallet-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-payby-wallet.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")   
def PayByWalletAmountTablePage(request):
    get_wallet = PayByWalletAmount.objects.filter(user__user_admin=request.user.refer_code)
    
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/pay-by-wallet-table.html", {'get_wallet':get_wallet,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeletePayByWalletAmount(request, id):
    cty = PayByWalletAmount.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/pay-by-wallet-table/")


@login_required(login_url="/admin-panel/")
def EditPayByWalletAmount(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletid"]   
        
          
        uplead = PayByWalletAmount.objects.filter(id=id)        
        uplead.update(user_id=gn, amount=mfp)
        messages.success(request, "Pay by wallet updated successfully")
        return redirect("/admin-panel/pay-by-wallet-table/") 
    else:
        getWallet = PayByWalletAmount.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-pay-by-wallet.html", {'getWallet':getWallet, 'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    


@login_required(login_url="/admin-panel/")   
def WithdrawalRequestCreate(request):
    if request.method == 'POST':
        usr = request.POST["user"]
        am = request.POST["amount"]  
        act = request.POST["actv"]      
        
        usr = WithdrawalRequest(user_id=usr, amount=am, payment_status=act,timestamp=datetime.now())
        usr.save()
        return redirect("/admin-panel/withdraw-request-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-withdraw-request.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    
@login_required(login_url="/admin-panel/")    
def WithdrawalRequestTablePage(request):
    get_withd = WithdrawalRequest.objects.filter(user__user_admin=request.user.refer_code)
    print("get_withd",get_withd, "Refer", request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/withdraw-request-table.html", {'get_withd':get_withd,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def DeleteWithdrawalRequest(request, id):
    cty = WithdrawalRequest.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/withdraw-request-table/")


@login_required(login_url="/admin-panel/")
def EditWithdrawalRequest(request, id):
    if request.method == 'POST':
        usr = request.POST["user"]
        am = request.POST["amount"]
        act = request.POST["actv"]

          
        uplead = WithdrawalRequest.objects.filter(id=id)   
        uplead.update(user_id=usr, amount=am, payment_status=act, timestamp=datetime.now())
        updated_withdrawal = WithdrawalRequest.objects.get(id=id)

        print("updated_withdrawal.payment_status", updated_withdrawal.payment_status)

        if updated_withdrawal.payment_status == True:
            tokens = [updated_withdrawal.user.device_registration_id]
            name = updated_withdrawal.user.first_name
            amt = updated_withdrawal.amount
            uid = updated_withdrawal.user.id
            # Create a message
            # message = messaging.MulticastMessage(
                
            #     notification=messaging.Notification(
            #         title='Withdrawal Request',
            #         body=f'Hello {name}! \n You are request has been successfully proceedings {amt} ',
            #         image= 'http://127.0.0.1:8000/Tambola/media/notification/notification.png'
            #     ),
                
                
            #     tokens=tokens,
            # )
            
            # response = messaging.send_multicast(message)
            # print("++++++++++",message.notification.body)
            
            # my_nitif = Notification(user_id=uid,title=message.notification.title, body=message.notification.body, image=message.notification.image)
            # my_nitif.save()
            
            messages.success(request, "Withdraw request updated successfully")
            return redirect("/admin-panel/withdraw-request-table/")
        else:
            pass
        messages.success(request, "Withdraw request updated successfully")
        return redirect("/admin-panel/withdraw-request-table/") 
    else:
        getWit = WithdrawalRequest.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-withdraw-request.html", {'getWit':getWit, 'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    
@login_required(login_url="/admin-panel/")
def KYCDetailsCreate(request):    
    if request.method == 'POST':
        user = request.POST["user"]
        aadharcard = request.FILES["aadharcard"]
        account_no = request.POST["account_no"]
        ifsc_code = request.POST["ifsc_code"]
        branch_name = request.POST["branch_name"]
        # is_verified = request.POST["is_verified"]
        
        if KYCDetails.objects.filter(account_no=account_no).exists():
            messages.info(request, 'KYC details already taken')
            return redirect('/admin-panel/new-kyc-detail/')
        else:
            usr = KYCDetails(user_id=user,aadharcard=aadharcard,account_no=account_no,ifsc_code=ifsc_code,branch_name=branch_name,is_verified=False)
            usr.save()
            return redirect("/admin-panel/kyc-detail-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-kyc-detail.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")
def KYCDetailsTablePage(request):
    get_kyc = KYCDetails.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/kyc-detail-table.html", {'get_kyc':get_kyc,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteKYCDetails(request, id):
    cty = KYCDetails.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/kyc-detail-table/")



@login_required(login_url="/admin-panel/")
def EditKYCDetailse(request, id):
    upleid = KYCDetails.objects.get(id=id)
    if request.method == 'POST':
        user = request.POST["user"]
        account_no = request.POST["account_no"]
        ifsc_code = request.POST["ifsc_code"]
        branch_name = request.POST["branch_name"]
        is_verified = request.POST["actv"]
        
        if len(request.FILES) !=0:
            if len(upleid.aadharcard) > 0:
                os.remove(upleid.aadharcard.path)
                print(upleid.aadharcard.path)
            upleid.aadharcard = request.FILES['aadharcard']
            
            upleid.save()
                
        uplead = KYCDetails.objects.filter(id=id)        
        uplead.update(user_id=user,account_no=account_no,ifsc_code=ifsc_code,branch_name=branch_name,is_verified=is_verified)
        messages.success(request, f"KYC detail updated successfully")
        return redirect("/admin-panel/kyc-detail-table/") 
    else:
        getKyc = KYCDetails.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-kyc-detail.html", {'kyc_detail':getKyc, 'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    
@login_required(login_url="/admin-panel/")  
def HelpAndSupportCreate(request):
    if request.method == 'POST':
        samtk = request.FILES["screenshot"]
        nm = request.POST["subject"]
        desc = request.POST["description"]        
        usr = request.POST['user']
        
        usr = HelpAndSupport(screenshot=samtk, subject=nm, description=desc, user_id=usr, created_at=datetime.now())
        usr.save()        
        return redirect("/admin-panel/help-support-table/")
    else:
        getUser = User.objects.filter(user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-help-support.html",{'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")    
def HelpAndSupportTablePage(request):
    get_rule = HelpAndSupport.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/help-support-table.html", {'get_rule':get_rule,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteHelpAndSupport(request, id):
    cty = HelpAndSupport.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/help-support-table/")


@login_required(login_url="/admin-panel/")
def EditHelpAndSupport(request, id):
    
    upleid = HelpAndSupport.objects.get(id=id)
    if request.method == 'POST':
        nm = request.POST["subject"]
        desc = request.POST["description"]        
        usr = request.POST['user']
        act = request.POST['actv']
        
        if len(request.FILES) !=0:
            if len(upleid.screenshot) > 0:
                os.remove(upleid.screenshot.path)
                print(upleid.screenshot.path)
            upleid.screenshot = request.FILES['screenshot']
            
            upleid.save()      
        uplead = HelpAndSupport.objects.filter(id=id)        
        uplead.update(subject=nm, description=desc, user_id=usr, is_completed=act)
        
        # updated_helpandsupport = HelpAndSupport.objects.get(id=id)

        # print("updated_withdrawal.is_completed", updated_helpandsupport.is_completed)

        # if updated_helpandsupport.is_completed == True:
        #     tokens = [updated_helpandsupport.user.device_registration_id]
        #     name = updated_helpandsupport.user.first_name
        #     uid = updated_helpandsupport.user.id
        #     # Create a message
        #     message = messaging.MulticastMessage(
                
        #         notification=messaging.Notification(
        #             title='Help & Support',
        #             body=f'Hello {name}! \n Your problem has been proceeding',
        #             image= 'http://127.0.0.1:8000/Tambola/media/notification/notification.png'
        #         ),
                
                
        #         tokens=tokens,
        #     )
            
        #     response = messaging.send_multicast(message)
        #     print("++++++++++",message.notification.body)
        #     my_nitif = Notification(user_id=uid,title=message.notification.title, body=message.notification.body, image=message.notification.image)
        #     my_nitif.save()
        messages.success(request, "Help Support updated successfully")
        return redirect("/admin-panel/help-support-table/") 
    else:
        getHelp = HelpAndSupport.objects.get(id=id)    
        getUser = User.objects.all()
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-help-support.html", {'getHelp':getHelp,'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    


@login_required(login_url="/admin-panel/")   
def NotificationCreate(request):
    if request.method == 'POST':
        usr = request.POST["user"]
        ti = request.POST["title"]
        msg = request.POST["body"]
        im = request.FILES["image"]        
        
        usr = Notification(user_id=usr, title=ti, body=msg, image=im, created_at=datetime.now())
        usr.save()
        return redirect("/admin-panel/notification-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-notification.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
    
@login_required(login_url="/admin-panel/")    
def NotificationTablePage(request):
    get_notif = Notification.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/notification-table.html", {'get_notif':get_notif,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def DeleteNotification(request, id):
    cty = Notification.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/notification-table/")


@login_required(login_url="/admin-panel/")
def EditNotification(request, id):
    uplead = Notification.objects.filter(id=id)        
    uplead.update(read_status=True)
    if request.method == 'POST':
        usr = request.POST["user"]
        ti = request.POST["title"]
        msg = request.POST["body"]
        act = request.POST["actv"]
        
        if len(request.FILES) !=0:
            if len(upleid.image) > 0:
                os.remove(upleid.image.path)
                print(upleid.image.path)
            upleid.image = request.FILES['image']
            
            upleid.save() 
          
        uplead = Notification.objects.filter(id=id)        
        uplead.update(user_id=usr, title=ti, body=msg, is_completed=act, created_at=datetime.now())
        
        
        updated_notification = Notification.objects.get(id=id)
        print("updated_notification", updated_notification.withdraw_req)
        
        
            
        print("updated_notification.is_completed", updated_notification.is_completed)

        if updated_notification.is_completed == True:
            
            tokens = [updated_notification.user.device_registration_id]
            name = updated_notification.user.first_name
            uid = updated_notification.user.id
            title = updated_notification.title
            # Create a message
            if title == "Withdrawal Request":
                # withdraw request status update
                updated_withdraw = WithdrawalRequest.objects.filter(id=updated_notification.withdraw_req.id)
                updated_withdraw.update(is_completed=True)
                print("updated_withdraw>>>>>>>>>")
                # message = messaging.MulticastMessage(
                    
                #     notification=messaging.Notification(
                #         title=f'{title}',
                #         body=f'Hello {name}! \n You are request has been successfully proceedings.',
                #         image= 'http://127.0.0.1:8000/Tambola/media/notification/notification.png'
                #     ),
                    
                    
                #     tokens=tokens,
                # )
                # response = messaging.send_multicast(message)
                # print("++++++++++",message.notification.body)
                # my_nitif = Notification(user_id=uid,title=message.notification.title, body=message.notification.body, image=message.notification.image)
                # my_nitif.save()
                
                messages.success(request, "compliment amount updated successfully")
            elif title == "Help & Support Request":
                # Help and support status update
                updated_help = HelpAndSupport.objects.filter(id=updated_notification.help_req.id)
                updated_help.update(is_completed=True)
                print("updated_Help & Support>>>>>>>>>")
                # message = messaging.MulticastMessage(
                    
                #     notification=messaging.Notification(
                #         title=f'{title}',
                #         body=f'Hello {name}! \n Your problem has been review success.',
                #         image= 'http://127.0.0.1:8000/Tambola/media/notification/notification.png'
                #     ),
                    
                    
                #     tokens=tokens,
                # )
            
                # response = messaging.send_multicast(message)
                # print("++++++++++",message.notification.body)
                # my_nitif = Notification(user_id=uid,title=message.notification.title, body=message.notification.body, image=message.notification.image)
                # my_nitif.save()
                
                messages.success(request, "compliment amount updated successfully")
            return redirect("/admin-panel/notification-table/")
        else:
            pass
        messages.success(request, "compliment amount updated successfully")
        return redirect("/admin-panel/notification-table/") 
    else:
        getNot = Notification.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False,is_staff=False,join_by_refer=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-notification.html", {'getNot':getNot, 'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")   
def ReferLinkSenderCreate(request):
    if request.method == 'POST':
        eml = request.POST["email"]
        gm = request.POST["game"]
        usr = request.POST["user"]       
        
        usr = ReferLinkSender(email=eml, user_id=usr, game_id=gm, created=datetime.now())
        usr.save()
        return redirect("/admin-panel/refer-link-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,join_by_refer=request.user.refer_code)
        getGame = Game.objects.filter(user__user_admin=request.user.refer_code)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-refer-link.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif,'getGame':getGame})
    
    
@login_required(login_url="/admin-panel/")    
def ReferLinkSenderTablePage(request):
    get_refer = ReferLinkSender.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/refer-link-table.html", {'get_refer':get_refer,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def DeleteReferLinkSender(request, id):
    ref = ReferLinkSender.objects.get(id=id)
    ref.delete()
    return redirect("/admin-panel/refer-link-table/")


@login_required(login_url="/admin-panel/")   
def ReferLinkSenderEdit(request, id):
    if request.method == 'POST':
        eml = request.POST["email"]
        gm = request.POST["game"]
        usr = request.POST["user"]       
        
        uplead = ReferLinkSender.objects.filter(id=id) 
        uplead.update(email=eml, user_id=usr, game_id=gm, created=datetime.now())
        messages.success(request, "Refer link updated successfully")
        return redirect("/admin-panel/refer-link-table/")
    else:
        getUser = User.objects.filter(is_superuser=False,is_staff=False,join_by_refer=request.user.refer_code)
        getGame = Game.objects.filter(user__user_admin=request.user.refer_code)
        ref_link = ReferLinkSender.objects.get(id=id) 
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-refer-link.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif,'getGame':getGame,'ref_link':ref_link})




@login_required(login_url="/admin-panel/")   
def FollowCreate(request):
    if request.method == 'POST':
        flw = request.POST["followed"]
        flw_by = request.POST["followed_by"]
        status = request.POST["actv"]       
        
        usr = Follow(followed_id=flw, followed_by_id=flw_by, muted=status, created_date=datetime.now())
        usr.save()
        return redirect("/admin-panel/follow-table/")
    else:
        getUser = User.objects.all()
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-follow.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")    
def FollowTablePage(request):
    get_flow = Follow.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    
    return render(request, "myadmin/follow-table.html", {'get_flow':get_flow,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})


@login_required(login_url="/admin-panel/")
def DeleteFollow(request, id):
    flw = Follow.objects.get(id=id)
    flw.delete()
    return redirect("/admin-panel/follow-table/")


@login_required(login_url="/admin-panel/")   
def FollowEdit(request, id):
    if request.method == 'POST':
        flw = request.POST["followed"]
        flw_by = request.POST["followed_by"]
        status = request.POST["actv"]      
        
        uplead = Follow.objects.filter(id=id) 
        uplead.update(followed_id=flw, followed_by_id=flw_by, muted=status, created_date=datetime.now())
        messages.success(request, "follow updated successfully")
        return redirect("/admin-panel/follow-table/")
    else:
        getUser = User.objects.all()
        follow = Follow.objects.get(id=id) 
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-follow.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif,'follow':follow})






@login_required(login_url="/admin-panel/")
def AddLanguageCreate(request):
    if request.method == 'POST':
        lang = request.POST["language"]
        if AddLanguage.objects.filter(language=lang).exists():
            messages.info(request, 'Language already taken')
            return redirect('/admin-panel/language-table/')
        else:   
            usr = AddLanguage(language=lang)
            usr.save()
            return redirect("/admin-panel/language-table/")
    else:
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-language.html", {'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")
def AddLanguageTablePage(request):
    get_lang = AddLanguage.objects.all()
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/language-table.html", {'get_lang':get_lang,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteAddLanguage(request, id):
    lang = AddLanguage.objects.get(id=id)
    lang.delete()
    return redirect("/admin-panel/language-table/")



@login_required(login_url="/admin-panel/")
def AddLanguageEdit(request, id):
    if request.method == 'POST':
        lang = request.POST['language']        
        uplead = AddLanguage.objects.filter(id=id)        
        uplead.update(language=lang)
        messages.success(request, f"{lang}, Language updated successfully")
        return redirect("/admin-panel/language-table/") 
    else:
        getLang = AddLanguage.objects.get(id=id)   
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-language.html", {'getLang':getLang,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    


@login_required(login_url="/admin-panel/")   
def CardDetailCreate(request):
    if request.method == 'POST':
        num = request.POST["card_number"]
        name = request.POST["card_holder_name"]
        exp_dt = request.POST["expiration_date"]     
        cv = request.POST["cvv"] 
        usr = request.POST["user"]   
        
        usr = CardDetail(card_number=num, card_holder_name=name, expiration_date=exp_dt, cvv=cv, user_id=usr, created_date=datetime.now())
        usr.save()
        return redirect("/admin-panel/card-detail-table/")
    else:
        getUser = User.objects.all()
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-card-detail.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def CardDetailTablePage(request):
    get_card = CardDetail.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/card-detail-table.html", {'get_card':get_card,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def DeleteCardDetail(request, id):
    card = CardDetail.objects.get(id=id)
    card.delete()
    return redirect("/admin-panel/card-detail-table/")


@login_required(login_url="/admin-panel/")
def CardDetailEdit(request, id):
    if request.method == 'POST':
        num = request.POST["card_number"]
        name = request.POST["card_holder_name"]
        exp_dt = request.POST["expiration_date"]     
        cv = request.POST["cvv"] 
        usr = request.POST["user"]        
        uplead = CardDetail.objects.filter(id=id)        
        uplead.update(card_number=num, card_holder_name=name, expiration_date=exp_dt, cvv=cv, user_id=usr, created_date=datetime.now())
        messages.success(request, "Card updated successfully")
        return redirect("/admin-panel/card-detail-table/") 
    else:
        getCard = CardDetail.objects.get(id=id)   
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-card-detail.html", {'getCard':getCard,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
        
    
    
@login_required(login_url="/admin-panel/")   
def GameCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]   
        point = request.POST["point_value"] 
        ply = request.POST["no_of_players"] 
        typ = request.POST["rummy_type"] 
        act = request.POST["actv"] 
        
        usr = Game1(user_id=gn,point_value=point,no_of_players=ply,rummy_type=typ,active=act,created_at=datetime.now())
        usr.save()
        return redirect("/admin-panel/game-table/")
    else:
        getUser = User.objects.all()
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-game.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    
@login_required(login_url="/admin-panel/")   
def GameTablePage(request):
    get_Game = Game1.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/game-table.html", {'get_Game':get_Game,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})

@login_required(login_url="/admin-panel/")
def DeleteGame(request, id):
    cty = Game1.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/game-table/")


@login_required(login_url="/admin-panel/")
def EditGame(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]   
        point = request.POST["point_value"] 
        ply = request.POST["no_of_players"] 
        typ = request.POST["rummy_type"] 
        act = request.POST["actv"]   
        
        uplead = Game1.objects.filter(id=id)        
        uplead.update(user_id=gn,point_value=point,no_of_players=ply,rummy_type=typ,active=act,created_at=datetime.now())
        messages.success(request, "Game updated successfully")
        return redirect("/admin-panel/game-table/") 
    else:
        getply = Game1.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-game.html", {'getply':getply, 'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    
    

@login_required(login_url="/admin-panel/")   
def SetCashLimitCreate(request):
    if request.method == 'POST':
        mina = request.POST["min_amount"]
        mont = request.POST["monthly_limit"]
        usr = request.POST["user"] 
        
        usr = SetCashLimit(min_amount=mina, monthly_limit=mont, user_id=usr)
        usr.save()
        return redirect("/admin-panel/cash-limit-table/")
    else:
        getUser = User.objects.all()
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/create-cash-limit.html", {'getUser':getUser,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def SetCashLimitTablePage(request):
    get_cash = SetCashLimit.objects.filter(user__user_admin=request.user.refer_code)
    num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
    num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
    num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
    notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
    return render(request, "myadmin/cash-limit-table.html", {'get_cash':get_cash,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})



@login_required(login_url="/admin-panel/")
def DeleteSetCashLimit(request, id):
    card = SetCashLimit.objects.get(id=id)
    card.delete()
    return redirect("/admin-panel/cash-limit-table/")


@login_required(login_url="/admin-panel/")
def SetCashLimitEdit(request, id):
    if request.method == 'POST':
        mina = request.POST["min_amount"]
        mont = request.POST["monthly_limit"]
        usr = request.POST["user"] 
                
        uplead = SetCashLimit.objects.filter(id=id)        
        uplead.update(min_amount=mina, monthly_limit=mont, user_id=usr)
        messages.success(request, "Card updated successfully")
        return redirect("/admin-panel/cash-limit-table/") 
    else:
        getcashlimit = SetCashLimit.objects.get(id=id)   
        num_help = HelpAndSupport.objects.filter(is_completed=False,user__user_admin=request.user.refer_code).count()
        num_withdraw = WithdrawalRequest.objects.filter(payment_status=False,user__user_admin=request.user.refer_code).count()
        num_notif = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code).count()
        notification = Notification.objects.filter(is_completed=False, read_status=False,user__user_admin=request.user.refer_code)
        return render(request, "myadmin/edit-cash-limit.html", {'getCash':getcashlimit,'notification':notification, 'num_help':num_help, 'num_withdraw':num_withdraw,'num_notif':num_notif})
    



    
