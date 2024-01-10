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
            if user.is_superuser:
                return redirect('/super-admin/index/')            
        else:
            messages.error(request, "Username or password incorrect")
            return redirect('/super-admin/')   
    else:
        return render(request, "mysuperadmin/page-login.html")


def logout_call(request):
    logout(request)
    return redirect('/super-admin/')


@login_required(login_url="/super-admin/")
def DashboardPage(request):
    notify = User.objects.filter(is_superuser=False).count()
    
    return render(request, "mysuperadmin/index.html", {"notify":notify})


# def ViewAdminProfile(request, id):
#     user = User.objects.get(id=id)
#     return render(request, "admin-profile.html", {'user':user})

@login_required(login_url="/super-admin/")
def UserTablePage(request):
    get_users = User.objects.filter(is_superuser=False)
    return render(request, "mysuperadmin/user-table.html", {"get_users":get_users})

@login_required(login_url="/super-admin/")
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
        
        birthdate_obj = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))
        
        print("age>>>>>>", age)
        if age >= 18:       
            if User.objects.filter(mobile_no=contact).exists():
                messages.error(request, 'Contact number already taken')
                return redirect('/super-admin/new-user/')
            else:
                usr = User(first_name=fname, username=uname, is_active=active, profile_picture=profile, mobile_no=contact,date_of_birth=dob, gender=gender, is_verified=vrfy,is_above18=above)
                usr.save()
                return redirect("/super-admin/users-table/")
        else:
            messages.error(request,"You are not Eligible")
            return redirect('/super-admin/new-user/')
    else:
        return render(request, "mysuperadmin/create-user.html")
    
        

@login_required(login_url="/super-admin/")
def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/super-admin/users-table/")



@login_required(login_url="/super-admin/")
def DetailUser(request, id):
    get_user = User.objects.get(id=id)
    
    
    return render(request, "mysuperadmin/app-profile.html", {'get_user':get_user})



@login_required(login_url="/super-admin/")
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
        return redirect("/super-admin/users-table/")
    else:
        getUser = User.objects.get(id=id)    
        return render(request, "mysuperadmin/edituser.html", {'user':getUser})
    
    
@login_required(login_url="/super-admin/") 
def ForgotPassword(request,id):
    # print('id',id)
    oldpwd=User.objects.get(id=id)
    # print('id',oldpwd.id)
    # print('kdfjv',oldpwd.password)
    if request.method == "POST":
        newpwd = request.POST['newpassword']
        uplead = User.objects.filter(id=id)
        uplead.update(password=make_password(newpwd))
        messages.success(request,"Password changed")
        logout(request)
        return redirect('/super-admin/')
    else:
        edtad=User.objects.get(id=id)
        # print(edtad)
        return render(request,'mysuperadmin/change-password.html',{'edtad':edtad, 'oldpwd':oldpwd})
    
    
    
    
@login_required(login_url="/super-admin/")
def StateCreate(request):
    if request.method == 'POST':
        state = request.POST["cty"]
        if State.objects.filter(name=state).exists():
            messages.info(request, 'State already taken')
            return redirect('/super-admin/state-table/')
        else:   
            usr = State(name=state)
            usr.save()
            return redirect("/super-admin/state-table/")
    else:
        return render(request, "mysuperadmin/create-state.html")
    
    
@login_required(login_url="/super-admin/")
def StateTablePage(request):
    get_state = State.objects.all()
    return render(request, "mysuperadmin/state-table.html", {'get_state':get_state})

@login_required(login_url="/super-admin/")
def DeleteState(request, id):
    cty = State.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/state-table/")



@login_required(login_url="/super-admin/")
def EditState(request, id):
    if request.method == 'POST':
        state = request.POST['cty']        
        uplead = State.objects.filter(id=id)        
        uplead.update(name=state)
        messages.success(request, f"{state}, State name updated successfully")
        return redirect("/super-admin/state-table/") 
    else:
        getState = State.objects.get(id=id)    
        return render(request, "mysuperadmin/create-state.html", {'state':getState})
    
    
    
    

@login_required(login_url="/super-admin/")
def KYCDetailsCreate(request):
    
    if request.method == 'POST':
        user = request.POST["user"]
        pancard = request.FILES["pancard"]
        aadharcard = request.FILES["aadharcard"]
        account_no = request.POST["account_no"]
        ifsc_code = request.POST["ifsc_code"]
        branch_name = request.POST["branch_name"]
        # is_verified = request.POST["is_verified"]
        
        if KYCDetails.objects.filter(pancard=pancard,aadharcard=aadharcard).exists():
            messages.info(request, 'KYC details already taken')
            return redirect('/super-admin/kyc-detail-table/')
        else:
            usr = KYCDetails(user_id=user,pancard=pancard,aadharcard=aadharcard,account_no=account_no,ifsc_code=ifsc_code,branch_name=branch_name,is_verified=False)
            usr.save()
            return redirect("/super-admin/kyc-detail-table/")
    else:
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/create-kyc-detail.html", {'getUser':getUser})
    
    
@login_required(login_url="/super-admin/")
def KYCDetailsTablePage(request):
    get_kyc = KYCDetails.objects.all()
    return render(request, "mysuperadmin/kyc-detail-table.html", {'get_kyc':get_kyc})

@login_required(login_url="/super-admin/")
def DeleteKYCDetails(request, id):
    cty = KYCDetails.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/kyc-detail-table/")



@login_required(login_url="/super-admin/")
def EditKYCDetailse(request, id):
    if request.method == 'POST':
        user = request.POST["user"]
        pancard = request.POST["pancard"]
        aadharcard = request.POST["aadharcard"]
        account_no = request.POST["account_no"]
        ifsc_code = request.POST["ifsc_code"]
        branch_name = request.POST["branch_name"]
        is_verified = request.POST["actv"]
                
        uplead = KYCDetails.objects.filter(id=id)        
        uplead.update(user_id=user,pancard=pancard,aadharcard=aadharcard,account_no=account_no,ifsc_code=ifsc_code,branch_name=branch_name,is_verified=is_verified)
        messages.success(request, f"KYC detail updated successfully")
        return redirect("/super-admin/kyc-detail-table/") 
    else:
        getKyc = KYCDetails.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-kyc-detail.html", {'kyc_detail':getKyc, 'getUser':getUser})
    
    
    
    

    
    


@login_required(login_url="/super-admin/")
def WalletAddCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletamount"]     
        rpoi = request.POST["actv"]      
        
        
        usr = WalletAdd(user_id=gn, walletamount=mfp, walletstatus=rpoi)
        usr.save()
        return redirect("/super-admin/wallet-add-table/")
    else:
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/create-wallet-add.html", {'getUser':getUser})
    
    
@login_required(login_url="/super-admin/")   
def WalletAddTablePage(request):
    get_wallet = WalletAdd.objects.all()
    return render(request, "mysuperadmin/wallet-add-table.html", {'get_wallet':get_wallet})

@login_required(login_url="/super-admin/")
def DeleteWalletAdd(request, id):
    cty = WalletAdd.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/wallet-add-table/")


@login_required(login_url="/super-admin/")
def EditWalletAdd(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletamount"]     
        rpoi = request.POST["actv"]
        
          
        uplead = WalletAdd.objects.filter(id=id)        
        uplead.update(user_id=gn, walletamount=mfp, walletstatus=rpoi)
        messages.success(request, "Wallet add updated successfully")
        return redirect("/super-admin/wallet-add-table/") 
    else:
        getWallet = WalletAdd.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-wallet-add.html", {'getWallet':getWallet, 'getUser':getUser})
    
    
@login_required(login_url="/super-admin/")   
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
        return redirect("/super-admin/wallet-amount-table/")
    else:
        getWallet = WalletAdd.objects.all()
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/create-wallet-amount.html", {'getUser':getUser,'getWallet':getWallet})
    
    
@login_required(login_url="/super-admin/")    
def WalletAmtTablePage(request):
    get_wallet = WalletAmt.objects.all()
    return render(request, "mysuperadmin/wallet-amount-table.html", {'get_wallet':get_wallet})

@login_required(login_url="/super-admin/")
def DetailWalletAmt(request, id):
    get_wallet = WalletAmt.objects.get(id=id)
    return render(request, "mysuperadmin/wallet-amount-detail.html", {'get_wallet':get_wallet})

@login_required(login_url="/super-admin/")
def DeleteWalletAmt(request, id):
    cty = WalletAmt.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/wallet-amount-table/")


@login_required(login_url="/super-admin/")
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
        return redirect("/super-admin/wallet-amount-table/") 
    else:
        getWalletadd = WalletAdd.objects.all()
        getWallet = WalletAmt.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-wallet-amount.html", {'getWallet':getWallet, 'getUser':getUser,'getWalletadd':getWalletadd})
    
    
    
    
@login_required(login_url="/super-admin/")   
def PayByWalletAmountCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletid"]      
        
        
        usr = PayByWalletAmount(user_id=gn, walletid=mfp)
        usr.save()
        return redirect("/super-admin/pay-by-wallet-table/")
    else:
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/create-payby-wallet.html", {'getUser':getUser})
    
    
@login_required(login_url="/super-admin/")   
def PayByWalletAmountTablePage(request):
    get_wallet = PayByWalletAmount.objects.all()
    return render(request, "mysuperadmin/pay-by-wallet-table.html", {'get_wallet':get_wallet})

@login_required(login_url="/super-admin/")
def DeletePayByWalletAmount(request, id):
    cty = PayByWalletAmount.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/pay-by-wallet-table/")


@login_required(login_url="/super-admin/")
def EditPayByWalletAmount(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletid"]   
        
          
        uplead = PayByWalletAmount.objects.filter(id=id)        
        uplead.update(user_id=gn, walletid=mfp)
        messages.success(request, "Pay by wallet updated successfully")
        return redirect("/super-admin/pay-by-wallet-table/") 
    else:
        getWallet = PayByWalletAmount.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-pay-by-wallet.html", {'getWallet':getWallet, 'getUser':getUser})
    

@login_required(login_url="/super-admin/")   
def WithdrawRequestCreate(request):
    if request.method == 'POST':
        usr = request.POST["user"]
        am = request.POST["amount"]  
        act = request.POST["actv"]      
        
        usr = WithdrawRequest(user_id=usr, amount=am, is_completed=act,created_at=datetime.now())
        usr.save()
        return redirect("/super-admin/withdraw-request-table/")
    else:
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/create-withdraw-request.html", {'getUser':getUser})
    
    
    
@login_required(login_url="/super-admin/")    
def WithdrawRequestTablePage(request):
    get_withd = WithdrawRequest.objects.all()
    return render(request, "mysuperadmin/withdraw-request-table.html", {'get_withd':get_withd})



@login_required(login_url="/super-admin/")
def DeleteWithdrawRequest(request, id):
    cty = WithdrawRequest.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/withdraw-request-table/")


@login_required(login_url="/super-admin/")
def EditWithdrawRequest(request, id):
    if request.method == 'POST':
        usr = request.POST["user"]
        am = request.POST["amount"]
        act = request.POST["actv"]

          
        uplead = WithdrawRequest.objects.filter(id=id)   
        uplead.update(user_id=usr, amount=am, is_completed=act, created_at=datetime.now())
        updated_withdrawal = WithdrawRequest.objects.get(id=id)

        print("updated_withdrawal.is_completed", updated_withdrawal.is_completed)

        if updated_withdrawal.is_completed == True:
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
            my_nitif = Notification(user_id=uid,title=message.notification.title, body=message.notification.body, image=message.notification.image)
            my_nitif.save()
            
            messages.success(request, "Withdraw request updated successfully")
            return redirect("/super-admin/withdraw-request-table/")
        else:
            pass
        messages.success(request, "Withdraw request updated successfully")
        return redirect("/super-admin/withdraw-request-table/") 
    else:
        getWit = WithdrawRequest.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-withdraw-request.html", {'getWit':getWit, 'getUser':getUser})
    
    
    

@login_required(login_url="/super-admin/")   
def PlayerCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]   
        
        
        usr = Player(user_id=gn)
        usr.save()
        return redirect("/super-admin/pay-by-wallet-table/")
    else:
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/create-payby-wallet.html", {'getUser':getUser})
    
    
@login_required(login_url="/super-admin/")   
def PlayerTablePage(request):
    get_player = Player.objects.all()
    return render(request, "mysuperadmin/player-table.html", {'get_player':get_player})

@login_required(login_url="/super-admin/")
def DeletePlayer(request, id):
    cty = Player.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/palyer-table/")


@login_required(login_url="/super-admin/")
def EditPlayer(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]  
        
          
        uplead = Player.objects.filter(id=id)        
        uplead.update(user_id=gn)
        messages.success(request, "Player updated successfully")
        return redirect("/super-admin/pay-by-wallet-table/") 
    else:
        getply = Player.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-player.html", {'getply':getply, 'getUser':getUser})
    
    
    
    
@login_required(login_url="/super-admin/")   
def GameCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]   
        
        
        usr = Game(user_id=gn)
        usr.save()
        return redirect("/super-admin/game-table/")
    else:
        getPly = Player.objects.all()
        
        return render(request, "mysuperadmin/create-game.html", {'getPly':getPly})
    
    
@login_required(login_url="/super-admin/")   
def GameTablePage(request):
    get_Game = Game.objects.all()
    return render(request, "mysuperadmin/game-table.html", {'get_Game':get_Game})

@login_required(login_url="/super-admin/")
def DeleteGame(request, id):
    cty = Game.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/game-table/")


@login_required(login_url="/super-admin/")
def EditGame(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]  
        
        uplead = Game.objects.filter(id=id)        
        uplead.update(user_id=gn)
        messages.success(request, "Game updated successfully")
        return redirect("/super-admin/game-table/") 
    else:
        getply = Game.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        return render(request, "mysuperadmin/edit-game.html", {'getply':getply, 'getUser':getUser})
    
    
    


@login_required(login_url="/super-admin/")   
def TournamentsCreate(request):
    if request.method == 'POST':
        gn = request.POST["name"]   
        des = request.POST["describe"]
        rei = request.POST["registration_ends_in"]
        win = request.POST["winners"]
        enp = request.POST["entry_point"]
        sd = request.POST["start_date"]
        nop = request.POST["num_of_player"]
        ti = request.FILES["tour_img"]
        usr = request.POST["user"]
        gm = request.POST["game"]
        
        usr = Tournaments(name=gn,describe=des,registration_ends_in=rei,winners=win,entry_point=enp,start_date=sd,num_of_player=nop,tour_img=ti,user_id=usr,game_id=gm,created=datetime.now())
        usr.save()
        return redirect("/super-admin/get_tournament-table/")
    else:
        getUser = User.objects.filter(is_superuser=False)
        getGame = Game.objects.all()
        return render(request, "mysuperadmin/create-tournament.html", {'getUser':getUser,'getGame':getGame})
    
    
@login_required(login_url="/super-admin/")   
def TournamentsTablePage(request):
    get_tournament = Tournaments.objects.all()
    return render(request, "mysuperadmin/tournament-table.html", {'get_tournament':get_tournament})

@login_required(login_url="/super-admin/")
def DetailTournaments(request, id):
    get_tourn = Tournaments.objects.get(id=id)
    return render(request, "mysuperadmin/tournament-detail.html", {'get_tourn':get_tourn})


@login_required(login_url="/super-admin/")
def DeleteTournaments(request, id):
    cty = Tournaments.objects.get(id=id)
    cty.delete()
    return redirect("/super-admin/get_tournament-table/")


@login_required(login_url="/super-admin/")
def EditTournaments(request, id):
    if request.method == 'POST':
        gn = request.POST["name"]   
        des = request.POST["describe"]
        rei = request.POST["registration_ends_in"]
        win = request.POST["winners"]
        enp = request.POST["entry_point"]
        sd = request.POST["start_date"]
        nop = request.POST["num_of_player"]
        # ti = request.FILES["tour_img"]
        usr = request.POST["user"]
        gm = request.POST["game"]
        
        uplead = Tournaments.objects.filter(id=id)        
        uplead.update(name=gn,describe=des,registration_ends_in=rei,winners=win,entry_point=enp,start_date=sd,num_of_player=nop,user_id=usr,game_id=gm)
        messages.success(request, "Game updated successfully")
        return redirect("/super-admin/get_tournament-table/") 
    else:
        getply = Tournaments.objects.get(id=id)    
        getUser = User.objects.filter(is_superuser=False)
        getGame = Game.objects.all()
        return render(request, "mysuperadmin/edit-tournament.html", {'getply':getply,'getUser':getUser,'getGame':getGame})