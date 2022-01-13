from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("create_account/", views.AccountCreateView.as_view(), name="account_create"),
    path("balance/", views.AccountBalanceView.as_view(), name="balance"),
    path("deposit/<str:username>/", views.DepositView.as_view(), name="deposit"),
    path("withdrawal/", views.WithdrawalView.as_view(), name="withdrawal"),
]
