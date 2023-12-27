from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
import datetime
import os
import string
import random

class State(models.Model):
    name  = models.CharField(max_length=300, null=True)

def filepath_profile(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('profile/', filename)

def generate_random_string():
    """Generate a random string of letters and digits."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class User(AbstractUser):
    profile_picture=models.FileField(upload_to=filepath_profile, default='profile/user.png')
    mobile_no = models.CharField(max_length=12, unique=True, null=True)
    middle_name = models.CharField(max_length=200, null=True)
    date_of_birth = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=300, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    pincode = models.CharField(max_length=300, null=True)
    is_verified=models.BooleanField(default=False)
    device_registration_id=models.CharField(max_length=500,null=True)
    is_above18=models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    refer_code=models.CharField(max_length=50,default=0)
    otp=models.CharField(max_length=50,null=True)
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    class Meta:
        db_table="customer"
   
    
    
class KYCDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pancard = models.CharField(max_length=100, unique=True)
    aadharcard = models.CharField(max_length=100, unique=True)
    account_no = models.CharField(max_length=100, unique=True)
    ifsc_code =  models.CharField(max_length=100)
    branch_name = models.CharField(max_length=300)
    is_verified=models.BooleanField(default=False)
    
    
    
    
class WalletAdd(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    walletamount=models.IntegerField()
    wallettime=models.DateTimeField(auto_now_add=True)
    walletstatus=models.BooleanField(default=False)

class WalletAmt(models.Model):
    walt = models.ForeignKey(WalletAdd,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    use_date = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    amount = models.CharField(max_length=200, null=True)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

class PayByWalletAmount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)