from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login),
    path('index/', views.DashboardPage),
    # path('changepassword/<int:id>/',views.ForgotPassword, name='changepass'),
    path('logout/', views.logout_call, name='logout'),
    
    path('new-user/', views.UserCreatePage),
    path('users-table/',views.UserTablePage),
    path('user-remove/<int:id>/', views.DeleteUser, name="user_del_by_ad"),
    path('user-edit/<int:id>/', views.EditUser, name="user_edit_by_ad"),
    path('user-detail/<int:id>/', views.DetailUser, name="view_detail_user_by_ad"),
    
    path('new-state/', views.StateCreate),
    path('state-table/', views.StateTablePage),
    path('state-remove/<int:id>/', views.DeleteState, name="city_del_by_ad"),
    path('state-edit/<int:id>/', views.EditState, name="city_edit_by_ad"),
    
    path('wallet-add-create/', views.WalletAddCreate),
    path('wallet-add-table/', views.WalletAddTablePage),
    path('wallet-add-remove/<int:id>/', views.DeleteWalletAdd, name="wallet_del_by_ad"),
    path('wallet-add-edit/<int:id>/', views.EditWalletAdd, name="wallet_edit_by_ad"), 
    
    path('wallet-amount-create/', views.WalletAmtCreate),
    path('wallet-amount-table/', views.WalletAmtTablePage),
    path('wallet-amount-remove/<int:id>/', views.DeleteWalletAmt, name="wallet_amt_del_by_ad"),
    path('wallet-amount-edit/<int:id>/', views.EditWalletAmt, name="wallet_amt_edit_by_ad"),
    path('wallet-amount-view-detail/<int:id>/', views.DetailWalletAmt, name="view_money_detail_by_ad"),
    
    path('pay-by-wallet-create/', views.PayByWalletAmountCreate),
    path('pay-by-wallet-table/', views.PayByWalletAmountTablePage),
    path('pay-by-wallet-remove/<int:id>/', views.DeletePayByWalletAmount, name="wallet_pay_del_by_ad"),
    path('pay-by-wallet-edit/<int:id>/', views.EditPayByWalletAmount, name="wallet_pay_edit_by_ad"),
    
    path('withdraw-request-create/', views.WithdrawRequestCreate),
    path('withdraw-request-table/', views.WithdrawRequestTablePage),
    path('withdraw-request-remove/<int:id>/', views.DeleteWithdrawRequest, name="wtdr_del_by_ad"),
    path('withdraw-request-edit/<int:id>/', views.EditWithdrawRequest, name="wtdr_edit_by_ad"),    
    
    path('new-kyc-detail/', views.KYCDetailsCreate),
    path('kyc-detail-table/', views.KYCDetailsTablePage),
    path('kyc-detail-remove/<int:id>/', views.DeleteKYCDetails, name="kyc_del_by_ad"),
    path('kyc-detail-edit/<int:id>/', views.EditKYCDetailse, name="kyc_edit_by_ad"),
    
    path('help-support-rule/', views.HelpAndSupportCreate),
    path('help-support-table/', views.HelpAndSupportTablePage),
    path('help-support-remove/<int:id>/', views.DeleteHelpAndSupport, name="help_del_by_ad"),
    path('help-support-edit/<int:id>/', views.EditHelpAndSupport, name="help_edit_by_ad"), 
    
    path('notification-create/', views.NotificationCreate),
    path('notification-table/', views.NotificationTablePage),
    path('notification-remove/<int:id>/', views.DeleteNotification, name="noiti_del_by_ad"),
    path('notification-edit/<int:id>/', views.EditNotification, name="noiti_edit_by_ad"),
    
    path('refer-link-create/', views.ReferLinkSenderCreate),
    path('refer-link-table/', views.ReferLinkSenderTablePage),
    path('refer-link-remove/<int:id>/', views.DeleteReferLinkSender, name="refer_del_by_ad"),
    path('refer-link-edit/<int:id>/', views.ReferLinkSenderEdit, name="refer_edit_by_ad"),
    
    path('follow-create/', views.FollowCreate),
    path('follow-table/', views.FollowTablePage),
    path('follow-remove/<int:id>/', views.DeleteFollow, name="flw_del_by_ad"),
    path('follow-edit/<int:id>/', views.FollowEdit, name="flw_edit_by_ad"),
    
    
    path('language-create/', views.AddLanguageCreate),
    path('language-table/', views.AddLanguageTablePage),
    path('language-remove/<int:id>/', views.DeleteAddLanguage, name="lang_del_by_ad"),
    path('language-edit/<int:id>/', views.AddLanguageEdit, name="lang_edit_by_ad"),
    
    path('card-detail-create/', views.CardDetailCreate),
    path('card-detail-table/', views.CardDetailTablePage),
    path('card-detail-remove/<int:id>/', views.DeleteCardDetail, name="card_del_by_ad"),
    path('card-detail-edit/<int:id>/', views.CardDetailEdit, name="card_edit_by_ad"),
    
    
    path('game-create/', views.GameCreate),
    path('game-table/', views.GameTablePage),    
    path('game-remove/<int:id>/', views.DeleteGame, name="game_del_by_ad"),
    path('game-edit/<int:id>/', views.EditGame, name="game_edit_by_ad"),
]