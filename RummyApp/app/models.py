from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
import datetime
import os
import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    user_admin=models.CharField(max_length=100)
    refer_code=models.CharField(max_length=50, unique=True)
    otp=models.CharField(max_length=50,null=True)
    join_by_refer = models.CharField(max_length=300, null=True)

    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    class Meta:
        db_table="customer"


@receiver(post_save, sender=User)
def generate_refer_code(sender, instance, created, **kwargs):
    # If the instance is newly created and the refer_code is not set, generate one
    if created and not instance.refer_code:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        instance.refer_code = instance.username[:4] + random_string
        instance.save()

def document(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('documents/', filename)
    
    

class KYCDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadharcard = models.ImageField(upload_to=document, null=False)
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


class WithdrawRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.CharField(max_length=100)
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)


class Player(models.Model):
    # name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.first_name
    

class Card(models.Model):
    rank = models.CharField(max_length=2)
    suit = models.CharField(max_length=10)
    
    def __str__(self):
        return self.rank

class Hand(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.card

class Game(models.Model):
    num_players = models.IntegerField()
    players = models.ManyToManyField(Player)
    draw_pile = models.ManyToManyField(Card, related_name='draw_pile')
    discard_pile = models.ManyToManyField(Card, related_name='discard_pile')
    

    
class GameRound(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_number = models.IntegerField()

class RoundHand(models.Model):
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return self.player.round.round_number
    


def filepath_Tournament(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('tournament/', filename)

class Tournaments(models.Model):
    name = models.CharField(max_length=200, null=True)
    describe = models.CharField(max_length=200, null=True)
    registration_ends_in = models.CharField(max_length=200, null=True)
    winners = models.CharField(max_length=200, null=True)
    entry_point = models.CharField(max_length=350, null=True)
    start_date = models.CharField(max_length=200, null=True)
    num_of_player = models.IntegerField()
    tour_img=models.FileField(upload_to=filepath_profile, default='tournament/Isolation_Mode.png')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    # entry_fee = models.DecimalField(max_digits=10, decimal_places=2)
    

# class JoinTournaments(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     tournament = models.ForeignKey(Tournaments,on_delete=models.CASCADE)
    
    
    

class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.timestamp}"
    


class CompleteYourKYC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=350, null=True)
    contact = models.CharField(max_length=350, null=True)
    email = models.EmailField(max_length=350, null=True)
    is_verified = models.BooleanField(default=False)
    
    
class HelpAndSupport(models.Model):
    subject=models.CharField(max_length=50)
    description=models.TextField()
    screenshot=models.FileField(upload_to ='helpandsupport', default='helpandsupport/helpandsupport.png')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject


def filepathNotif(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('notification/', filename)
class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    body=models.TextField()
    image=models.FileField(upload_to =filepathNotif, default='notification/notification.png')
    is_completed=models.BooleanField(default=False)
    read_status=models.BooleanField(default=False)
    withdraw_req=models.ForeignKey(WithdrawRequest,on_delete=models.CASCADE, null=True)
    help_req=models.ForeignKey(HelpAndSupport,on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now=True)

    
class ReferLinkSender(models.Model):
    email = models.EmailField(max_length=300,null=True)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)



class Follow(models.Model):
    followed = models.ForeignKey(User, related_name='user_followers', on_delete=models.CASCADE)
    followed_by = models.ForeignKey(User, related_name='user_follows', on_delete=models.CASCADE)
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed_by.username} started following {self.followed.username}"





class AddLanguage(models.Model):
    language = models.CharField(max_length=100, unique=True)
    
    
class CardDetail(models.Model):
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.card_number
    
    
class SetCashLimit(models.Model):
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    
class TimeLimite(models.Model):
    time = models.CharField(max_length=100, unique=True)
    
class SetDailtTimeLimit(models.Model):
    daily_time = models.ForeignKey(TimeLimite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)