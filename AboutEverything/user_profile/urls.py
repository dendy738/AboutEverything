from django.urls import path
from .views import profile_info, change_password, user_posts


urlpatterns = [
    path('<int:user_id>/', profile_info, name='profile'),
    path('<int:user_id>/passwords/', change_password, name='change_password'),
    path('<int:user_id>/user_posts/', user_posts, name='user_posts'),
]
