from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    # note : for login view you need to connect it to a template name.
    # once you log out it goes to the homepage by default.
    # but note that we specify the (LOGIN_REDIRECT_URL) and (LOGOUT_REDIRECT_URL) into settings.py
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.SignUp.as_view(), name='signup')
]
