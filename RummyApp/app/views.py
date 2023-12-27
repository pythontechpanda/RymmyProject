from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
import string
import random
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        print(">>>>>",user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    
# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request):
#         user_data = request.data.copy()

#         # Generate username based on mobile number and a random string
#         random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
#         random_string_var =str(random_string)
        
#         username = f"{user_data['mobile_no'][:4]}{random_string_var}"
#         user_data['username'] = username

#         # Set the password the same as the username
#         user_data['password'] = username

#         serializer = self.serializer_class(data=user_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data

#         return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        usr =  User.objects.get(username=request.data['username'])
        print('usr', usr.is_above18)
        if usr.is_above18 == True:
            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(">>>>>>>>>>>",serializer.data['device_registration_id'])
            tokens = [serializer.data['device_registration_id']]
            name = serializer.data['username']
            otp = serializer.data['otp']
            # Create a message from firebase
            
            # message = messaging.MulticastMessage(
                
            #     notification=messaging.Notification(
            #         title='Tambola Invitation',
            #         body=f'Hello {name}! \n You are Otp is: {otp}',
            #         image= 'http://127.0.0.1:8000/media/notification/notification.png'
            #     ),
                
                
            #     tokens=tokens,
            # )
            
            # response = messaging.send_multicast(message)
            # print(response)
            
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("Your not authenticated user")
    
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'msg': 'Logout Successfully'},status=status.HTTP_200_OK)
    
    

class KYCDetailsView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = KYCDetails.objects.all()
        serializer = KYCDetailsSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = KYCDetails.objects.get(id=id)
            serializer = KYCDetailsSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = KYCDetailsSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = KYCDetails.objects.get(pk=id)
        serializer = KYCDetailsSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = KYCDetails.objects.get(pk=id)
        serializer = KYCDetailsSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = KYCDetails.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})



class WalletAddView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = WalletAdd.objects.all()
        serializer = WalletAddSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = WalletAdd.objects.get(id=id)
            serializer = WalletAddSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = WalletAddSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
            print(">>>>>>", client)
            payment = client.order.create({ 'amount': float(serializer.data['walletamount'])*100, 'currency': 'INR', 'payment_capture': 1})
            print("******************************")
            print(payment['amount'])
            print("******************************")
            return Response({'msg': 'Data Created','order_id':payment['id'],'user_id':serializer.data['user'],'status':serializer.data['walletstatus']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = WalletAdd.objects.get(pk=id)
        serializer = WalletAddSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = WalletAdd.objects.get(pk=id)
        serializer = WalletAddSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = WalletAdd.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
class WalletAmtView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = WalletAmt.objects.all()
        serializer = WalletAmtSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = WalletAmt.objects.get(id=id)
            serializer = WalletAmtSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = WalletAmtSerializer(data = request.data)  # form data conviert in json data
        print("request.data",request.data['amount'])
        prod = WalletAmt.objects.filter(user=request.data['user'])
        tik = BuyTicket.objects.filter(userid=request.data['user'])
        his = 0
        for j in tik:
            print("ticket", j)
            his += float(j.order_price)
        print("history", his)
        
        c = 0
        for i in prod:
            c = c + float(i.amount)
            print(i.amount)
        print("amount",c, request.data['amount'])
    
        uss=PayByWalletAmount.objects.filter(user=request.data['user']).exists()
        print('hcawdskj',uss)
        am = float(c)+float(request.data['amount'])-float(his)
        if uss:
            var2=PayByWalletAmount.objects.filter(user=request.data['user'])
            var2.update(amount=am)
        else:
            print(am)
            var1 = PayByWalletAmount(user_id=request.data['user'], amount=am)
            var1.save()
        if serializer.is_valid():
            serializer.save()
            print("====================",serializer.data['user'])
            
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = WalletAmt.objects.get(pk=id)
        serializer = WalletAmtSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = WalletAmt.objects.get(pk=id)
        serializer = WalletAmtSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = WalletAmt.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})


    
class PayByWalletAmountView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = PayByWalletAmount.objects.all()
        serializer = PayByWalletAmountSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = PayByWalletAmount.objects.get(id=id)
            serializer = PayByWalletAmountSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = PayByWalletAmountSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = PayByWalletAmount.objects.get(pk=id)
        serializer = PayByWalletAmountSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = PayByWalletAmount.objects.get(pk=id)
        serializer = PayByWalletAmountSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = PayByWalletAmount.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

