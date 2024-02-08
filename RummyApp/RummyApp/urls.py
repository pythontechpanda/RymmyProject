"""
URL configuration for RummyApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views
from django.conf import settings  
from django.conf.urls.static import static


router = DefaultRouter()

router.register('KYC-detail', views.KYCDetailsView, basename='KYC-detail'),
router.register('WalletAdd', views.WalletAddView, basename='WalletAdd'),
router.register('WalletAmt', views.WalletAmtView, basename='WalletAmt'),
router.register('PayByWalletAmount', views.PayByWalletAmountView, basename='PayByWalletAmount'),
# router.register('players', views.PlayerViewSet, basename='players')
# router.register('cards', views.CardViewSet, basename='cards')
# router.register('decks', views.DeckViewSet, basename='decks')
# router.register('rummygames', views.RummyGameViewSet, basename='rummygames')
router.register('tournament', views.TournamentsView, basename='tournament')
router.register('withdrawal-request', views.WithdrawalRequestView, basename='withdrawal-request')
router.register('complete-your-kyc', views.CompleteYourKYCView, basename='complete-your-kyc')
router.register('follow', views.FollowView, basename='follow')
router.register('edit-user-details', views.EditRegisterUserView, basename='edit-user-details')
router.register('refer-link', views.ReferelLinkSenderView, basename='refer-link')
router.register('Language', views.AddLanguageView, basename='Language')
router.register('card-detail', views.CardDetailView, basename='card-detail')
router.register('set-cash-limit', views.SetCashLimitView, basename='set-cash-limit')
router.register('time-limit', views.TimeLimiteView, basename='time-limit')
router.register('set-time-limit', views.SetDailtTimeLimitView, basename='set-time-limit')
router.register('spin-prize', views.SpinView, basename='spin-prize')
router.register('declare', views.DeclareView, basename='declare')
router.register('finish', views.FinishView, basename='finish')
router.register('sort', views.SortItView, basename='sort')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('super-admin/', include("my_superadmin.urls")),
    path('admin-panel/', include("my_admin.urls")),
    path('api/', include("app.urls")),
]


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 