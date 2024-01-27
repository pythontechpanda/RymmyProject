from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import random
class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'profile_picture', 'first_name', 'middle_name', 'last_name', 'email','city', 'state', 'pincode', 'gender','date_of_birth','mobile_no','is_verified', 'is_above18', 'is_user','device_registration_id','join_by_refer']
    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
        
        
class EditRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'profile_picture', 'first_name', 'middle_name', 'last_name', 'email','city', 'state', 'refer_code', 'pincode', 'gender','date_of_birth','mobile_no','is_verified', 'is_above18', 'is_user','device_registration_id','join_by_refer','user_admin']
    
    
    
    
class LoginSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()
    otp = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    def get_otp(self, obj):
        randomNumber = random.randint(1000, 9999)
        return randomNumber
    class Meta:
        model = User
        fields = ['id','username', 'profile_picture', 'first_name', 'middle_name', 'last_name', 'email','city', 'state', 'pincode', 'gender','date_of_birth','mobile_no','is_verified', 'is_above18', 'is_user','otp','tokens','device_registration_id']
    def validate(self, attrs):
        username = attrs.get('username','')
        # password = attrs.get('password','')
        try:
            user = User.objects.get(username=username)
            # if not user.is_active:
            #     raise AuthenticationFailed('Account disabled, contact admin')
            if not user.is_above18:
                raise AuthenticationFailed('Age must be minimum of 18 years')
            return {
                'id': user.id,
                'first_name': user.first_name,
                'username': user.username,
                'profile_picture':user.profile_picture,
                'city':user.city,
                'state':user.state,
                'pincode':user.pincode,
                'gender':user.gender,
                'date_of_birth':user.date_of_birth,
                'mobile_no':user.mobile_no,
                'is_verified':user.is_verified,
                'is_above18':user.is_above18,
                'refer_code':user.refer_code,
                'tokens': user.tokens,
                'device_registration_id': user.device_registration_id
            }
        except:
            raise AuthenticationFailed('Invalid credentials, try again')
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
            
            
            
class KYCDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDetails
        fields = ['id','user','aadharcard','account_no','ifsc_code','branch_name','is_verified']
        
class WalletAddSerializer(serializers.ModelSerializer):
    # user = RegisterSerializer()
    class Meta:
        model = WalletAdd
        fields = '__all__'

class WalletAmtSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAmt
        fields = '__all__'

class PayByWalletAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayByWalletAmount
        fields = '__all__'
        
        
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

# class DeckSerializer(serializers.ModelSerializer):
#     cards = CardSerializer(many=True)

#     class Meta:
#         model = Deck
#         fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    # deck = DeckSerializer()

    class Meta:
        model = Game
        fields = '__all__'
        
        
        
class TournamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournaments
        fields = '__all__'
        
        
class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'
    

class CompleteYourKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompleteYourKYC
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
    

class ReferLinkSenderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReferLinkSender
        fields = ['id','email','game','created','user']
        
        
        
class AddLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddLanguage
        fields = '__all__'
        
        
class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetail
        fields = '__all__'
        
        
class SetCashLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetCashLimit
        fields = '__all__'
        
        
class TimeLimiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLimite
        fields = '__all__'
        
        
class SetDailtTimeLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetDailtTimeLimit
        fields = '__all__'
        
        
        
        
class UserFilterSerializer(serializers.Serializer):
    aadharcard=serializers.IntegerField()
    account_no=serializers.ImageField()
    ifsc_code=serializers.CharField(max_length=255)
    branch_name=serializers.CharField(max_length=25)
    is_verified=serializers.CharField(max_length=25)
    
    walt=serializers.CharField(max_length=255)
    use_date=serializers.DateTimeField()
    payment_status=serializers.BooleanField()
    amount=serializers.CharField(max_length=255)
    razor_pay_order_id=serializers.CharField(max_length=255)
    razor_pay_payment_id=serializers.CharField(max_length=255)
    razor_pay_payment_signature=serializers.CharField(max_length=255)
    
    user_id= serializers.IntegerField()
    profile_picture= serializers.FileField()
    username= serializers.CharField(max_length=255)
    mobile_no=serializers.CharField(max_length=255)
    first_name=serializers.CharField(max_length=255)
    middle_name=serializers.CharField(max_length=255)
    last_name=serializers.CharField(max_length=255)
    date_of_birth=serializers.CharField(max_length=255)
    
    city=serializers.CharField(max_length=255)
    state=serializers.CharField(max_length=255)
    pincode=serializers.CharField(max_length=255)   
    gender=serializers.CharField(max_length=255)
    is_verified=serializers.BooleanField()
    is_above18=serializers.BooleanField()
    refer_code=serializers.CharField(max_length=255)
    join_by_refer=serializers.CharField(max_length=255)
    is_user=serializers.CharField(max_length=255)
    user_admin=serializers.CharField(max_length=255)
    device_registration_id=serializers.CharField(max_length=255)
    created=serializers.IntegerField()