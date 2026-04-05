from django.db import models
from users.models import UserModel

# Create your models here.


class PostCategory(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    slug_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Posts(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    post_category = models.ForeignKey(PostCategory, on_delete=models.CASCADE)
    author_id = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, default='Unknown')
    reports_quantity = models.PositiveIntegerField(default=0)


class Comments(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class Likes(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class Dislikes(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

