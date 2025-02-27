
from django.urls import path
from authentication.views import LoginView,RegisterView,CustomTokenRefreshView,CustomTokenVerifyView,StockView
# from rest_framework_simplejwt.views import (
#     TokenVerifyView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('stock/', StockView.as_view(), name='stock'),

]

