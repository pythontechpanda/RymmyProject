from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.DashboardPage),
    path('', views.Login),
    # path('view-admin-profile/<int:id>/', views.ViewAdminProfile, name="admin_profile"),
    path('changepassword/<int:id>/',views.ForgotPassword, name='changepass'),
    path('logout/', views.logout_call, name='logout'),
    
    path('new-user/', views.UserCreatePage),
    path('users-table/',views.UserTablePage),
    path('user-remove/<int:id>/', views.DeleteUser, name="user_del"),
    path('user-edit/<int:id>/', views.EditUser, name="user_edit"),
    path('user-detail/<int:id>/', views.DetailUser, name="view_detail_user"),
    path('admin-user-get/<int:id>/', views.AdminUserTablePage, name="get_player"),
    
    path('new-state/', views.StateCreate),
    path('state-table/', views.StateTablePage),
    path('state-remove/<int:id>/', views.DeleteState, name="city_del"),
    path('state-edit/<int:id>/', views.EditState, name="city_edit"),
    
    path('new-kyc-detail/', views.KYCDetailsCreate),
    path('kyc-detail-table/', views.KYCDetailsTablePage),
    path('kyc-detail-remove/<int:id>/', views.DeleteKYCDetails, name="kyc_del"),
    path('kyc-detail-edit/<int:id>/', views.EditKYCDetailse, name="kyc_edit"),
    
    
    
    path('wallet-add-create/', views.WalletAddCreate),
    path('wallet-add-table/', views.WalletAddTablePage),
    path('wallet-add-remove/<int:id>/', views.DeleteWalletAdd, name="wallet_del"),
    path('wallet-add-edit/<int:id>/', views.EditWalletAdd, name="wallet_edit"), 
    
    path('wallet-amount-create/', views.WalletAmtCreate),
    path('wallet-amount-table/', views.WalletAmtTablePage),
    path('wallet-amount-remove/<int:id>/', views.DeleteWalletAmt, name="wallet_amt_del"),
    path('wallet-amount-edit/<int:id>/', views.EditWalletAmt, name="wallet_amt_edit"),
    path('wallet-amount-view-detail/<int:id>/', views.DetailWalletAmt, name="view_money_detail"),
    
    
    path('pay-by-wallet-create/', views.PayByWalletAmountCreate),
    path('pay-by-wallet-table/', views.PayByWalletAmountTablePage),
    path('pay-by-wallet-remove/<int:id>/', views.DeletePayByWalletAmount, name="wallet_pay_del"),
    path('pay-by-wallet-edit/<int:id>/', views.EditPayByWalletAmount, name="wallet_pay_edit"),
    
    path('withdraw-request-create/', views.WithdrawRequestCreate),
    path('withdraw-request-table/', views.WithdrawRequestTablePage),
    path('withdraw-request-remove/<int:id>/', views.DeleteWithdrawRequest, name="wtdr_del"),
    path('withdraw-request-edit/<int:id>/', views.EditWithdrawRequest, name="wtdr_edit"),
    
    path('palyer-create/', views.PlayerCreate),
    path('palyer-table/', views.PlayerTablePage),
    path('palyer-remove/<int:id>/', views.DeletePlayer, name="ply_del"),
    path('palyer-edit/<int:id>/', views.EditPlayer, name="ply_edit"),
    
    path('game-create/', views.GameCreate),
    path('game-table/', views.GameTablePage),    
    path('game-remove/<int:id>/', views.DeleteGame, name="game_del"),
    path('game-edit/<int:id>/', views.EditGame, name="game_edit"),
    
    path('tournament-create/', views.TournamentsCreate),
    path('get_tournament-table/', views.TournamentsTablePage),
    path('tournament-detail/<int:id>/', views.DetailTournaments, name="view_tour"),
    path('tournament-remove/<int:id>/', views.DeleteTournaments, name="tour_del"),
    path('tournament-edit/<int:id>/', views.EditTournaments, name="tour_edit"),
    
    path('help-support-rule/', views.HelpAndSupportCreate),
    path('help-support-table/', views.HelpAndSupportTablePage),
    path('help-support-remove/<int:id>/', views.DeleteHelpAndSupport, name="help_del"),
    path('help-support-edit/<int:id>/', views.EditHelpAndSupport, name="help_edit"), 
    
    path('notification-create/', views.NotificationCreate),
    path('notification-table/', views.NotificationTablePage),
    path('notification-remove/<int:id>/', views.DeleteNotification, name="noiti_del"),
    path('notification-edit/<int:id>/', views.EditNotification, name="noiti_edit"),
]