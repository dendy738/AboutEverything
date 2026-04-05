from django.urls import path
from .views import user_signup, user_auth, get_email, user_password_update


urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('signin/', user_auth, name='signin'),
    path('passwords/', get_email, name='get_email'),
    path('passwords/<int:user_id>/', user_password_update, name='upd_pass')
]
