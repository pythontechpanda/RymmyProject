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
from django.core.mail import send_mail
import string
import random
# Create your views here.

def generate_random_string():
    """Generate a random string of letters and digits."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        print(">>>>>",user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # here get refer code to getting user_admin
        get_admin = User.objects.get(refer_code=serializer.data["join_by_refer"])
        # here get refer by admin code
        usr_admin = get_admin.user_admin
        print("usr_admin>>>", usr_admin)
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Create the refer_code using the first 4 characters of the username and the random string
        refcode = get_admin.username[:4] + random_string
        print("refcode", refcode)
        
        # now new user which we have register by using refer code there user_admin code update new user user_admin field
        uplead = User.objects.filter(id=serializer.data["id"])
        uplead.update(user_admin=usr_admin)
        
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
        
        


class EditRegisterUserView(viewsets.ViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
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

#         # Create two decks
#         deck1 = create_deck()
#         deck2 = create_deck()
        
#         # Concatenate the decks
#         combined_deck = deck1 + deck2

#         draw_pile = [Card.objects.create(rank=card['rank'], suit=card['suit']) for card in combined_deck]
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
        game.players.set(selected_users)  # Use set to associate users with the game

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
            "player_names": [player.username for player in selected_users],  # Use 'username' instead of 'user.username'
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
            # Check if there is a card available
            if card:
                game.draw_pile.remove(card)
                round_hand = RoundHand.objects.create(round=game_round, player=player, card=card)
                
                if player.first_name not in hands_data:
                    hands_data[player.first_name] = []

                hands_data[player.first_name].append({
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
        player_name = hand.player.username
        card_info = {'rank': hand.card.rank, 'suit': hand.card.suit}
        if player_name not in hands:
            hands[player_name] = [card_info]
        else:
            hands[player_name].append(card_info)

    return JsonResponse({"hands": hands})

@api_view(['POST'])
def draw_card(request, game_id, player_id):
    game = Game.objects.get(pk=game_id)
    player = User.objects.get(pk=player_id)
    game_round = GameRound.objects.filter(game_id=game_id).latest('round_number')

    if not game.draw_pile.exists():
        game.draw_pile.set(Card.objects.filter(roundhand__round=game_round))

    card = game.draw_pile.first()
    game.draw_pile.remove(card)
    RoundHand.objects.create(round=game_round, player=player, card=card)

    return JsonResponse({"message": f"{player.username} drew a card: {card.rank} of {card.suit}"})



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
            print("Data stored")
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


class WithdrawalAmountByUserFilterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):

        if User.objects.filter(id=id).exists():
            obj = WithdrawalRequest.objects.filter(user=id,payment_status=True)
            print(obj)
            amt = 0
            for i in obj:
                amt = amt + i.amount
            

            return Response({'WithdrawAmount': amt})
        else:
            raise AuthenticationFailed('Invalid ID, try again')




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
            obj=Follow.objects.filter(followed_id=id, muted=False)
            print("obj", obj)
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
        


class ReferelLinkSenderView(viewsets.ViewSet):
    def list(self, request):      # list - get all record
        stu = ReferLinkSender.objects.all()
        serializer = ReferLinkSenderSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = ReferLinkSender.objects.get(id=id)
            serializer = ReferLinkSenderSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = ReferLinkSenderSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            user = request.user.refer_code            
            email_address = serializer.data['email']
            send_mail(
            'Response Mail',
            f'Hi  \nI am thrilled to invite you for a Real Rummy task at our office.\nVia Real Rummy so that we can get know you better. your task schedule is Today.\nhttps://realrummy.hirectjob.in/userrefercode/{user} ',
            'pythontechpanda@gmail.com',
            [email_address],
            fail_silently=False,
            )
            return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        id = pk
        stu = ReferLinkSender.objects.get(pk=id)
        serializer = ReferLinkSenderSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = ReferLinkSender.objects.get(pk=id)
        serializer = ReferLinkSenderSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = ReferLinkSender.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
    
class AddLanguageView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = AddLanguage.objects.all()
        serializer = AddLanguageSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = AddLanguage.objects.get(id=id)
            serializer = AddLanguageSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = AddLanguageSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = AddLanguage.objects.get(pk=id)
        serializer = AddLanguageSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = AddLanguage.objects.get(pk=id)
        serializer = AddLanguageSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = AddLanguage.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
    
class CardDetailView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = CardDetail.objects.all()
        serializer = CardDetailSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = CardDetail.objects.get(id=id)
            serializer = CardDetailSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = CardDetailSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = CardDetail.objects.get(pk=id)
        serializer = CardDetailSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = CardDetail.objects.get(pk=id)
        serializer = CardDetailSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = CardDetail.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
    
    
class SetCashLimitView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = SetCashLimit.objects.all()
        serializer = SetCashLimitSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = SetCashLimit.objects.get(id=id)
            serializer = SetCashLimitSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = SetCashLimitSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = SetCashLimit.objects.get(pk=id)
        serializer = SetCashLimitSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = SetCashLimit.objects.get(pk=id)
        serializer = SetCashLimitSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = SetCashLimit.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
class TimeLimiteView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = TimeLimite.objects.all()
        serializer = TimeLimiteSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = TimeLimite.objects.get(id=id)
            serializer = TimeLimiteSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = TimeLimiteSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = TimeLimite.objects.get(pk=id)
        serializer = TimeLimiteSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = TimeLimite.objects.get(pk=id)
        serializer = TimeLimiteSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = TimeLimite.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})



class SetDailtTimeLimitView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = SetDailtTimeLimit.objects.all()
        serializer = SetDailtTimeLimitSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = SetDailtTimeLimit.objects.get(id=id)
            serializer = SetDailtTimeLimitSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = SetDailtTimeLimitSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = SetDailtTimeLimit.objects.get(pk=id)
        serializer = SetDailtTimeLimitSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = SetDailtTimeLimit.objects.get(pk=id)
        serializer = SetDailtTimeLimitSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = SetDailtTimeLimit.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
    
    
    
class UserFilterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            kyc_details = KYCDetails.objects.get(user=user)
            wallet = PayByWalletAmount.objects.get(user=user)

            # Assuming User model has fields like 'username', 'mobile_no', etc.
            user_data = {
                'user_id': user.id,
                'profile_picture': user.profile_picture.url,
                'username': user.username,
                'mobile_no': user.mobile_no,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'city': user.city,
                'state': user.state,
                'pincode': user.pincode,
                'gender': user.gender,
                'is_verified': user.is_verified,
                'is_above18': user.is_above18,
                'refer_code': user.refer_code,
                'join_by_refer': user.join_by_refer,
                'is_user': user.is_user,
                'user_admin': user.user_admin,
                'device_registration_id': user.device_registration_id,
                # 'created': user.created,
            }

            kyc_details_data = {}
            kyc_details_data.update({
                'id': kyc_details.id,
                'aadharcard': kyc_details.aadharcard.url,
                'account_no': kyc_details.account_no,
                'ifsc_code': kyc_details.ifsc_code,
                'branch_name': kyc_details.branch_name,
                'is_verified_kyc': kyc_details.is_verified,
            })

            wallet_data = {}
            
            wallet_data.update({
                'id': wallet.id,
                'amount': wallet.amount,
                
            })
            # print("wallet_data",wallet_data)
            # print("kyc_details_data",kyc_details_data)
            user_data['kyc_details'] = kyc_details_data
            user_data['wallet_data'] = wallet_data

            serializer = UserFilterSerializer(data=user_data)
            # serializer.is_valid()

            return Response({'profile': user_data})

        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid ID, try again')
        
        

class SpinView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Spin.objects.all()
        serializer = SpinSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Spin.objects.get(id=id)
            serializer = SpinSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = SpinSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Spin.objects.get(pk=id)
        serializer = SpinSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Spin.objects.get(pk=id)
        serializer = SpinSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Spin.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})        
        

class SpinFilterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):

        if User.objects.filter(id=id).exists():
            # Filter Follow objects where followed is the specified user and muted is True
            obj = Spin.objects.filter(user=id)
            created_serializer = SpinFilterSerializer(obj, many=True)

            return Response({'Spin-Prizes': created_serializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')



class ReferLinkFilterView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, id):

        if User.objects.filter(id=id).exists():
            # Filter Follow objects where followed is the specified user and muted is True
            obj = ReferLinkSender.objects.filter(user=id)
            print(obj)
            created_serializer = ReferLinkFilterSenderSerializer(obj, many=True)

            return Response({'Refer-filter': created_serializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')




class DeclareView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Declare.objects.all()
        serializer = DeclareSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Declare.objects.get(id=id)
            serializer = DeclareSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = DeclareSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Declare.objects.get(pk=id)
        serializer = DeclareSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Declare.objects.get(pk=id)
        serializer = DeclareSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Declare.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'}) 
    
    
class FinishView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Finish.objects.all()
        serializer = FinishSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Finish.objects.get(id=id)
            serializer = FinishSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = FinishSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Finish.objects.get(pk=id)
        serializer = FinishSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Finish.objects.get(pk=id)
        serializer = FinishSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Finish.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'}) 
    
    
class SortItView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = SortIt.objects.all()
        serializer = SortItSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = SortIt.objects.get(id=id)
            serializer = SortItSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = SortItSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            # Access and manipulate the serialized data before saving
            serialized_data = serializer.validated_data
            print("Serialized Data:", serialized_data)
            

            # Sort the list of cards based on the card_suit sequence
            sorted_cards = sorted(serialized_data['listofcards'], key=lambda card: card['card_suit'])

            # Update the serialized data with the sorted cards
            serialized_data['listofcards'] = sorted_cards
            serializer.save()
            
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = SortIt.objects.get(pk=id)
        serializer = SortItSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = SortIt.objects.get(pk=id)
        serializer = SortItSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = SortIt.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'}) 