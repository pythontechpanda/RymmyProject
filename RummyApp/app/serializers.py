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
        fields = ['id','username', 'profile_picture', 'first_name', 'middle_name', 'last_name', 'email','city', 'state', 'refer_code', 'pincode', 'gender','date_of_birth','mobile_no','is_verified', 'is_above18', 'is_user','device_registration_id']
    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
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
        fields = ['id','username', 'profile_picture', 'first_name', 'middle_name', 'last_name', 'email','city', 'state', 'refer_code', 'pincode', 'gender','date_of_birth','mobile_no','is_verified', 'is_above18', 'is_user','otp','tokens','device_registration_id']
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
        fields = ['id','user','pancard','aadharcard','account_no','ifsc_code','branch_name','is_verified']
        
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

    

# class ReferLinkSenderSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = ReferLinkSender
#         fields = '__all__'