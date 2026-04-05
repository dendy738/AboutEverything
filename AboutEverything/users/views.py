from django.db import IntegrityError, DatabaseError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from .forms import UserRegistrationForm, UserAuthorizationForm, UserEmailForm, UserNewPasswordForm
from .models import UserModel
from .data_validation import UserDataValidator, ValidationError
from .encrypt import get_encrypted, password_compare
from main_app.login_decorator import is_logged




def user_signup(request):
    messages.set_level(request, messages.INFO)
    if request.method == 'GET':
        store = messages.get_messages(request)
        store.is_used = True
        form = UserRegistrationForm()
        return render(request, 'users/signup.html', {'form': form})
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                UserDataValidator(**data)
            except ValidationError as e:
                messages.error(request, e)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                try:
                    UserModel.objects.create(
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        second_last_name=data['second_last_name'],
                        birthday=data['birthday'],
                        user_name=data['user_name'],
                        password=get_encrypted(data['password']),
                        email=data['email'],
                        country=data['country'],
                        contact_number=data['contact_number'],
                    )
                except IntegrityError:
                    messages.error(request, 'User already exists.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except DatabaseError:
                    messages.error(request, 'Something went wrong! Please try again later.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.success(request, 'Your registration is successful! You can log in now.')
                    return HttpResponseRedirect(reverse('signin'))
        else:
            messages.error(request, 'Data not valid.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Action not allowed.')


@is_logged
def user_auth(request):
    messages.set_level(request, messages.INFO)
    if request.method == 'GET':
        form = UserAuthorizationForm()
        return render(request, 'users/signin.html', {'form': form})
    elif request.method == 'POST':
        form = UserAuthorizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                user = UserModel.objects.get(user_name=data['username'])
            except UserModel.DoesNotExist:
                messages.error(request, 'User not found.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                if password_compare(data['password'], user.password):
                    request.session['user'] = user.id
                    request.session['is_authenticated'] = True

                    response =  HttpResponseRedirect(f'/posts')
                    response.set_cookie('user_name', user.user_name)
                    return response
                else:
                    messages.error(request, 'Incorrect password.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Data are not valid.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Action not allowed.')


def get_email(request):
    if request.method == 'GET':
        email_form = UserEmailForm()
        return render(request, 'users/email.html', {'form': email_form})
    elif request.method == 'POST':
        email_form = UserEmailForm(request.POST)
        if email_form.is_valid():
            data = email_form.cleaned_data

            try:
                user = UserModel.objects.get(email=data['email'])
            except UserModel.DoesNotExist:
                messages.error(request, 'User with such email does not exist.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(f'/users/passwords/{user.id}')
        else:
            messages.error(request, 'Invalid email.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Action not allowed.')


def user_password_update(request, user_id):
    if request.method == 'GET':
        pass_form = UserNewPasswordForm()
        return render(request, 'users/upd_pass.html', {'form': pass_form})
    elif request.method == 'POST':
        pass_form = UserNewPasswordForm(request.POST)
        if pass_form.is_valid():
            data = pass_form.cleaned_data

            try:
                UserDataValidator(**data)
            except ValidationError as e:
                messages.error(request, e)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                pass

            try:
                UserModel.objects.filter(id=user_id).update(password=get_encrypted(data['password']))
            except UserModel.NotUpdated:
                messages.error(request, 'Password not being changed.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except IntegrityError:
                messages.error(request, 'Password not being changed.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except DatabaseError:
                messages.error(request, 'Something went wrong! Please try again later.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('signin'))
        else:
            messages.error(request, 'Data are not valid.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Action not allowed.')