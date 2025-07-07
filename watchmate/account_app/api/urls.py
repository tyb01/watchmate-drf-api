from account_app.api.views import RegisterView , LogoutView

from rest_framework.authtoken import views
from django.urls import path


urlpatterns = [
    path('login/', views.obtain_auth_token, name="login" ),
    path('register/', RegisterView, name="register" ),
    path('logout/', LogoutView, name="logout" ),

]
