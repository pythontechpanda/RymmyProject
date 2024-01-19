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
]