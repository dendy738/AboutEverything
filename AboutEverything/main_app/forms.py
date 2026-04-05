from django import forms
from django.db import DatabaseError
from users.models import UserModel
from .models import PostCategory, Posts, Comments



class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'post_category']
        widgets = {
            'post_category': forms.Select
        }


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=1000, label='Your comment')

    def save_comment(self, author_id, post_id):
        try:
            Comments.objects.create(
                content=self.cleaned_data['content'],
                author=UserModel.objects.get(id=author_id),
                post=Posts.objects.get(id=post_id)
            )
        except DatabaseError:
            return 'Something went wrong. Please try again later.', 500
        else:
            return 'Comment submitted.', 200


class ChangePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'post_category']

