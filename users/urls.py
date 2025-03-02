from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'), #post
    path('login/', views.LoginView.as_view(), name='login'), #post
    path('logout/', views.LogoutView.as_view(), name='logout'), #post
    path('verify/email/<str:token>/', views.Activate),
    path('token-refresh/', views.RefreshTokenView.as_view(), name='token_refresh'), #post
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'), #put
    path('customer-profile/', views.CustomerProfileView.as_view(), name='update-profile'), #patch, get
]