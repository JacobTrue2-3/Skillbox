from django.urls import path
from .views import get_cookie_view, set_cookie_view, set_session_view, get_session_view, MylogoutView, AboutMeView, RegisterView
from django.contrib.auth.views import LoginView


app_name = 'myauth'

urlpatterns = [
    # path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(template_name="myauth/login.html", redirect_authenticated_user=True), name='login'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('cookie/get', get_cookie_view, name='cookie-get'),
    path('session/set/', set_session_view, name='session-set'),
    path('session/get/', get_session_view, name='session-get'),
    # path('logout/', logout_view, name='logout'),
    path('logout/', MylogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('register/', RegisterView.as_view(), name='register'),
]
