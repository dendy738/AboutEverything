from django.urls import path
from .views import main_page, add_post, logout, post_review, add_like, add_dislike, add_comment, post_edit, post_delete, delete_comment, filter_by_category

urlpatterns = [
    path('', main_page, name='posts'),
    path('add/', add_post, name='add_post'),
    path('logout/', logout, name='logout'),
    path('<int:post_id>/', post_review, name='show_post'),
    path('<int:post_id>/likes/', add_like, name='add_like'),
    path('<int:post_id>/dislikes/', add_dislike, name='add_dislike'),
    path('<int:post_id>/comments/add/', add_comment, name='add_comment'),
    path('<int:post_id>/comments/<int:comment_id>/', delete_comment, name='del_comment'),
    path('<int:post_id>/edit/', post_edit, name='edit_post'),
    path('<int:post_id>/del/', post_delete, name='del_post'),
    path('<str:cat_name>/', filter_by_category, name='category_filter'),
]
