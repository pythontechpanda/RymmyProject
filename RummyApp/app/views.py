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
from RummyApp import settings
import razorpay
from django.http import JsonResponse
from rest_framework.decorators import api_view

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
    
    
    
class EditRegisterUserView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = User.objects.all()
        serializer = EditRegisterSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = User.objects.get(id=id)
            serializer = EditRegisterSerializer(stu)
            return Response(serializer.data)

    # def create(self, request):
    #     serializer = EditRegisterSerializer(data = request.data)  # form data conviert in json data
    #     if serializer.is_valid():
    #         serializer.save()            
    #         return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = EditRegisterSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = EditRegisterSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
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
        # tik = BuyTicket.objects.filter(userid=request.data['user'])
        his = 0
        # for j in tik:
        #     print("ticket", j)
        #     his += float(j.order_price)
        # print("history", his)
        
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



class GetWalletAmountView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        print("user id: ",id)
        if User.objects.filter(id=id).exists():
            obj=WalletAmt.objects.filter(user=id)
            print("=========>>>>",obj)
            c = 0
            for i in obj:
                print(i)
                c = c + float(i.amount)
                
            uss=PayByWalletAmount.objects.filter(user=id).exists()
            if uss:
                var2=PayByWalletAmount.objects.get(user=id)
                chg=var2.amount
            else:
                chg=0

            return Response({'Available Balance': c})
        else:
            raise AuthenticationFailed('Invalid ID, try again')







# @api_view(['GET'])
# def start_game(request, num_players):
#     game = Game.objects.create(num_players=num_players)
#     players = [Player.objects.create(user=f"Player {i+1}") for i in range(num_players)]
#     game.players.set(players)

#     deck = create_deck()
#     draw_pile = [Card.objects.create(rank=card['rank'], suit=card['suit']) for card in deck]
#     game.draw_pile.set(draw_pile)
    
    
#     response_data = {
#         "message": "Game started successfully!",
#         "num_players": num_players,
#         "player_names": [player.name for player in players],
#         "draw_pile": [{"rank": card.rank, "suit": card.suit} for card in draw_pile],
#     }

#     return JsonResponse(response_data)






# class start_game(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     def get(self,request, num_players):
#         if num_players < 2 or num_players > 6:
#             response_data = {
#                 "message": "Invalid number of players. Allowed range: 2 to 6 players.",
#             }
#             return JsonResponse(response_data, status=400)  

#         game = Game.objects.create(num_players=num_players)
        
#         gm_players = User.objects.all()[:num_players]  # Limit the number of players to the desired value
#         players = []

#         for ply in gm_players:
#             player = Player.objects.create(user=ply)
#             players.append(player)
        
#         game.players.set(players)

#         deck = create_deck()
#         draw_pile = [Card.objects.create(rank=card['rank'], suit=card['suit']) for card in deck]
#         game.draw_pile.set(draw_pile)
        
#         response_data = {
#             "message": "Game started successfully!",
#             "num_players": num_players,
#             "player_names": [player.user.username for player in players],
#             "draw_pile": [{"rank": card.rank, "suit": card.suit} for card in draw_pile],
#         }

#         return JsonResponse(response_data)



# class start_game(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, num_players):
#         if num_players < 2 or num_players > 6:
#             response_data = {
#                 "message": "Invalid number of players. Allowed range: 2 to 6 players.",
#             }
#             return JsonResponse(response_data, status=400)

#         all_users = list(User.objects.filter(is_user=True))
        
#         if len(all_users) < num_players:
#             response_data = {
#                 "message": "Not enough users available for the requested number of players.",
#             }
#             return JsonResponse(response_data, status=400)

#         selected_users = random.sample(all_users, num_players)

#         game = Game.objects.create(num_players=num_players)
#         players = []

#         for selected_user in selected_users:
#             player = Player.objects.create(user=selected_user)
#             players.append(player)

#         game.players.set(players)

#         deck = create_deck()
#         draw_pile = [Card.objects.create(rank=card['rank'], suit=card['suit']) for card in deck]
#         game.draw_pile.set(draw_pile)

#         response_data = {
#             "message": "Game started successfully!",
#             "num_players": num_players,
#             "player_names": [player.user.username for player in players],
#             "draw_pile": [{"rank": card.rank, "suit": card.suit} for card in draw_pile],
#         }

#         return JsonResponse(response_data)


class start_game(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, num_players):
        if num_players < 2 or num_players > 6:
            response_data = {
                "message": "Invalid number of players. Allowed range: 2 to 6 players.",
            }
            return JsonResponse(response_data, status=400)

        all_users = list(User.objects.filter(is_user=True))
        
        if len(all_users) < num_players:
            response_data = {
                "message": "Not enough users available for the requested number of players.",
            }
            return JsonResponse(response_data, status=400)

        selected_users = random.sample(all_users, num_players)

        game = Game.objects.create(num_players=num_players)
        players = []

        for selected_user in selected_users:
            player = Player.objects.create(user=selected_user)
            players.append(player)

        game.players.set(players)

        # Create two decks
        deck1 = create_deck()
        deck2 = create_deck()
        
        # Concatenate the decks
        combined_deck = deck1 + deck2

        draw_pile = [Card.objects.create(rank=card['rank'], suit=card['suit']) for card in combined_deck]
        game.draw_pile.set(draw_pile)

        response_data = {
            "message": "Game started successfully!",
            "num_players": num_players,
            "player_names": [player.user.username for player in players],
            "draw_pile": [{"rank": card.rank, "suit": card.suit} for card in draw_pile],
        }

        return JsonResponse(response_data)


def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck



@api_view(['POST'])
def deal_hands(request, game_id):
    game = Game.objects.get(pk=game_id)
    game_round = GameRound.objects.create(game=game, round_number=1)
    hands_data = {}
    for _ in range(13):
        for player in game.players.all():
            card = game.draw_pile.first()
            print("player>>>>>>>>>>", player.user.first_name)
            # Check if there is a card available
            if card:
                game.draw_pile.remove(card)
                round_hand = RoundHand.objects.create(round=game_round, player=player, card=card)
                
                if player.user.first_name not in hands_data:
                    hands_data[player.user.first_name] = []

                hands_data[player.user.first_name].append({
                    'card_id': round_hand.card.id,
                    'card_suit': round_hand.card.suit,
                    'card_rank': round_hand.card.rank,
                })
            else:
                # Handle the case when there are no cards in the draw pile
                return JsonResponse({"message": "Not enough cards in the draw pile!"}, status=400)

    return JsonResponse({"message": "Hands dealt successfully!", "hands_data": hands_data})



@api_view(['GET'])
def display_hands(request, game_id):
    game_round = GameRound.objects.filter(game_id=game_id).latest('round_number')
    hands = {}
    for hand in RoundHand.objects.filter(round=game_round):
        player_name = hand.player.user.username
        card_info = {'rank': hand.card.rank, 'suit': hand.card.suit}
        if player_name not in hands:
            hands[player_name] = [card_info]
        else:
            hands[player_name].append(card_info)

    return JsonResponse({"hands": hands})

@api_view(['POST'])
def draw_card(request, game_id, player_id):
    game = Game.objects.get(pk=game_id)
    player = Player.objects.get(pk=player_id)
    game_round = GameRound.objects.filter(game_id=game_id).latest('round_number')

    if not game.draw_pile.exists():
        game.draw_pile.set(Card.objects.filter(roundhand__round=game_round))

    card = game.draw_pile.first()
    game.draw_pile.remove(card)
    RoundHand.objects.create(round=game_round, player=player, card=card)

    return JsonResponse({"message": f"{player.user} drew a card: {card.rank} of {card.suit}"})



class TournamentsView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Tournaments.objects.all()
        serializer = TournamentsSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Tournaments.objects.get(id=id)
            serializer = TournamentsSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = TournamentsSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Tournaments.objects.get(pk=id)
        serializer = TournamentsSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Tournaments.objects.get(pk=id)
        serializer = TournamentsSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Tournaments.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
    
    
    
class WithdrawalRequestView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = WithdrawalRequest.objects.all()
        serializer = WithdrawalRequestSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = WithdrawalRequest.objects.get(id=id)
            serializer = WithdrawalRequestSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = WithdrawalRequestSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = WithdrawalRequest.objects.get(pk=id)
        serializer = WithdrawalRequestSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = WithdrawalRequest.objects.get(pk=id)
        serializer = WithdrawalRequestSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = WithdrawalRequest.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})



class CompleteYourKYCView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = CompleteYourKYC.objects.all()
        serializer = CompleteYourKYCSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = CompleteYourKYC.objects.get(id=id)
            serializer = CompleteYourKYCSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = CompleteYourKYCSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = CompleteYourKYC.objects.get(pk=id)
        serializer = CompleteYourKYCSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = CompleteYourKYC.objects.get(pk=id)
        serializer = CompleteYourKYCSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = CompleteYourKYC.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})





class FollowView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Follow.objects.all()
        serializer = FollowSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Follow.objects.get(id=id)
            serializer = FollowSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = FollowSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Follow.objects.get(pk=id)
        serializer = FollowSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Follow.objects.get(pk=id)
        serializer = FollowSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Follow.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
    
class FollowRequestFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
         
        if User.objects.filter(id=id).exists():
            obj=Follow.objects.filter(followed=id, muted=False)
            createdserializer = FollowSerializer(obj,many=True)

            return Response({'FollowRequest':createdserializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        
        
class FollowRequestAcceptFilterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):

        if User.objects.filter(id=id).exists():
            # Filter Follow objects where followed is the specified user and muted is True
            obj = Follow.objects.filter(followed=id, muted=True)
            created_serializer = FollowSerializer(obj, many=True)

            return Response({'FollowRequest': created_serializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        


# Refer link
# class ReferLinkSenderView(viewsets.ViewSet):
#     def list(self, request):      # list - get all record
#         stu = ServeyLinkSenders.objects.all()
#         serializer = ServeyLinkSenderSerializer(stu, many=True)    # many use for bulk data come 
#         return Response(serializer.data)


#     def retrieve(self, request, pk=None):
#         id = pk
#         if id is not None:
#             stu = ServeyLinkSenders.objects.get(id=id)
#             serializer = ServeyLinkSenderSerializer(stu)
#             return Response(serializer.data)

#     def create(self, request):
#         serializer = ServeyLinkSenderSerializer(data = request.data)  # form data conviert in json data
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.data)
#             qustionId = serializer.data['servey']
#             email_address = serializer.data['email']
#             send_mail(
#             'Response Mail',
#             f'Hi  \nI am thrilled to invite you for a Shadev Ai task at our office.\nVia Shadev AI so that we can get know you better. your task schedule is Today.\nhttps://jobteam.hirectjob.in/surveymakeremail/{qustionId} ',
#             'pythontechpanda@gmail.com',
#             [email_address],
#             fail_silently=False,
#             )
#             return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def update(self, request, pk):
#         id = pk
#         stu = ServeyLinkSenders.objects.get(pk=id)
#         serializer = ServeyLinkSenderSerializer(stu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Complete Data Update'})
#         return Response(serializer.errors)

#     def partial_update(self, request, pk):
#         id = pk
#         stu = ServeyLinkSenders.objects.get(pk=id)
#         serializer = ServeyLinkSenderSerializer(stu, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Partial Data Update'})
#         return Response(serializer.errors)

#     def destroy(self, request, pk):
#         id = pk
#         stu = ServeyLinkSenders.objects.get(pk=id)
#         stu.delete()
#         return Response({'msg': 'Data deleted'})



class HomeFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        current_dateTime = datetime.datetime.now()
        if User.objects.filter(id=id).exists():
            
            obj=Tournaments.objects.all()
            upcoming=[]
            utc=pytz.UTC
            for i in obj:
                upcomingdetail={}
                start_time = current_dateTime.replace(tzinfo=utc)
                end_time =i.start_at.replace(tzinfo=utc)
                if end_time > start_time:
                    objcount=Tournaments.objects.filter(user_id=i.user.id).count()

                    played_ticket=Game.objects.filter(user_id=i.user.id)
                    played=[]
                    for j in played_ticket:
                        if j.game in played:
                            pass
                        else:
                            played.append(j.game)
                   
                    upcomingdetail.update({'game_id':i.id,
                                           'game_name':i.game_name,
                                           'message_for_player':i.message_for_player,
                                           'lobby':i.lobby,
                                           'ticket_cost':i.ticket_cost,
                                           'start_at':i.start_at,
                                           'ticket_request_till':i.ticket_request_till,
                                           'number_of_ticket':i.number_of_tickets,
                                           'timer':i.timer,
                                           'private_code':i.private_code,
                                        #    'game_counter':i.game_counter,
                                           'is_completed':i.is_completed,
                                        #    'created_at':i.created_at,
                                           'user_id': i.user.id,
                                            'first_name': i.user.first_name,
                                            'username': i.user.username,
                                            'profile_picture':i.user.profile_picture,
                                            'city':i.user.city.city_name,
                                            'gender':i.user.gender,
                                            'date_of_birth':i.user.date_of_birth,
                                            'mobile_no':i.user.mobile_no,
                                            'is_verified':i.user.is_verified,
                                            'is_above18':i.user.is_above18,
                                            'refer_code':i.user.refer_code,
                                            'refer_by':i.user.refer_by,
                                            'my_code':i.user.my_code,
                                            'played':len(played),
                                            'created':objcount})
                    upcoming.append(upcomingdetail)
            print('upcoming',upcoming)
            up= UpcomingSerializer(upcoming,many=True)

            live=[]
            for k in obj:
                livedetail={}
                start_time = current_dateTime.replace(tzinfo=utc)
                end_time =k.start_at.replace(tzinfo=utc)
                if end_time < start_time and k.is_completed==False:                   
                    # live.append(k)
                    obj=NewGame.objects.filter(user_id=k.user.id).count()

                    played_ticket=Ticket.objects.filter(assign_to_id=k.user.id)
                    played=[]
                    for j in played_ticket:
                        if j.game in played:
                            pass
                        else:
                            played.append(j.game)
                   
                    livedetail.update({'game_id':k.id,
                                           'game_name':k.game_name,
                                           'message_for_player':k.message_for_player,
                                           'lobby':k.lobby,
                                           'ticket_cost':k.ticket_cost,
                                           'start_at':k.start_at,
                                           'ticket_request_till':k.ticket_request_till,
                                           'number_of_ticket':k.number_of_tickets,
                                           'timer':k.timer,
                                           'private_code':k.private_code,
                                        #    'game_counter':k.game_counter,
                                           'is_completed':k.is_completed,
                                        #    'created_at':k.created_at,
                                           'user_id': k.user.id,
                                            'first_name': k.user.first_name,
                                            'username': k.user.username,
                                            'profile_picture':k.user.profile_picture,
                                            'city':k.user.city.city_name,
                                            'gender':k.user.gender,
                                            'date_of_birth':k.user.date_of_birth,
                                            'mobile_no':k.user.mobile_no,
                                            'is_verified':k.user.is_verified,
                                            'is_above18':k.user.is_above18,
                                            'refer_code':k.user.refer_code,
                                            'refer_by':k.user.refer_by,
                                            'my_code':k.user.my_code,
                                            'played':len(played),
                                            'created':obj})
                    live.append(livedetail)
            liveserializer = LiveSerializer(live,many=True)
            
            return Response({'Upcoming':up.data,'Live':liveserializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')