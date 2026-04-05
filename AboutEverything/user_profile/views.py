from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from .forms import ProfileForm

from users.models import UserModel
from users.data_validation import UserDataValidator, ValidationError
from users.forms import UserNewPasswordForm
from users.encrypt import get_encrypted

from main_app.login_decorator import is_logged
from main_app.models import Posts



@is_logged
def profile_info(request, user_id):
    user = UserModel.objects.get(id=user_id)
    if request.method == 'GET':
        profile = ProfileForm(instance=user)
        return render(request, 'user_profile/profile.html', {'form': profile, 'user_id': user_id})
    elif request.method == 'POST':
        profile = ProfileForm(request.POST, instance=user)
        if profile.is_valid():
            try:
                profile.save()
            except DatabaseError:
                messages.error(request, 'Something went wrong.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Profile updated successfully.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@is_logged
def change_password(request, user_id):
    if request.method == 'GET':
        form = UserNewPasswordForm()
        return render(request, 'user_profile/change_pass.html', {'form': form, 'user_id': user_id})
    elif request.method == 'POST':
        form = UserNewPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                UserDataValidator(**data)
            except ValidationError as e:
                messages.error(request, e)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            try:
                UserModel.objects.filter(id=user_id).update(password=get_encrypted(data['password']))
            except IntegrityError:
                messages.error(request, 'Something went wrong! Please try again later.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except DatabaseError:
                messages.error(request, 'Something went wrong! Please try again later.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Password updated successfully!')
                return HttpResponseRedirect(reverse('profile', args=[user_id]))
        else:
            messages.error(request, 'Incorrect data!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Method not allowed.')


@is_logged
def user_posts(request, user_id):
    if request.method == 'GET':
        user_posts = Posts.objects.filter(author_id=user_id).order_by('-posted_at')
        return render(request, 'user_profile/user_posts.html', {'us_posts': user_posts, 'user_id': user_id})


