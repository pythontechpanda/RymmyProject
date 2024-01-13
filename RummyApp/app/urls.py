from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('wallet-amount/<int:id>/',views.GetWalletAmountView.as_view(),name="walletamt"),
    
    path('start_game/<int:num_players>/', views.start_game.as_view(), name='start_game'),
    path('deal_hands/<int:game_id>/', views.deal_hands, name='deal_hands'),
    path('display_hands/<int:game_id>/', views.display_hands, name='display_hands'),
    path('draw_card/<int:game_id>/<int:player_id>/', views.draw_card, name='draw_card'),
    path('follow-request-filter/<int:id>/',views.FollowRequestFilterView.as_view(),name="follow-request-filter"),
    path('follow-request-accept-filter/<int:id>/',views.FollowRequestAcceptFilterView.as_view(),name="follow-request-accept-filter"),
]