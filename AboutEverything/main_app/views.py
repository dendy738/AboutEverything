from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .models import Comments, PostCategory, Posts, Likes, Dislikes
from .login_decorator import is_logged
from .forms import PostForm, CommentForm, ChangePostForm
from users.models import UserModel
import asyncio
from .censure_api.censure_check import main_check_profanity



categories = PostCategory.objects.all()

def search_post(request):
    search_query = request.GET.get('search', None)
    if search_query:
        satisfy_posts = Posts.objects.filter(title__icontains=search_query).order_by('-posted_at')
        context = {
            'posts': satisfy_posts,
            'categories': categories,
            'user_id': request.session.get('user'),
        }
        return render(request, 'main_app/main_page.html', context=context)
    return None


@is_logged
def main_page(request):
    search_response = search_post(request)
    if search_response is None:
        last_5 = Posts.objects.all().order_by('-posted_at')[:5]
        context = {
            'posts': last_5,
            'categories': categories,
            'user_id': request.session.get('user')
        }
        return render(request, 'main_app/main_page.html', context=context)
    else:
        return search_response


@is_logged
def filter_by_category(request, cat_name):
    certain_posts = Posts.objects.filter(post_category__slug_name=cat_name).order_by('-posted_at')
    context = {
        'posts': certain_posts,
        'categories': categories,
        'user_id': request.session.get('user'),
    }
    return render(request, 'main_app/main_page.html', context=context)


@is_logged
def add_post(request):
    user = UserModel.objects.get(id=request.session.get('user'))
    if request.method == 'GET':
        post_form = PostForm()
        context = {
            'form': post_form,
            'categories': categories,
            'user_id': request.session.get('user')
        }
        return render(request, 'main_app/new_post.html', context=context)
    elif request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            data = post_form.cleaned_data

            if asyncio.run(main_check_profanity(data['title'], data['content'])):
                messages.error(request, 'Post contains obscene language.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            try:
                post = post_form.save(commit=False)
                post.author_id = user
                post.save()
            except DatabaseError:
                messages.error(request, 'Something went wrong. Please try again later.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Post submitted.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'The fields must be filled according to filling rules.')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseBadRequest('Method not allowed.')


@is_logged
def post_review(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
        likes = Likes.objects.filter(post=post_id)
        dislikes = Dislikes.objects.filter(post=post_id)
        comments = Comments.objects.filter(post=post_id)
    except Posts.DoesNotExist:
        return HttpResponseNotFound('Post does not exist.')
    else:
        pass

    if request.method == 'GET':
        comment = CommentForm()
        context = {
            'post': post,
            'comment_form': comment,
            'categories': categories,
            'user_id': request.session.get('user'),
            'likes': len(likes),
            'dislikes': len(dislikes),
            'comments': comments,
        }
        return render(request, 'main_app/post.html', context=context)


@is_logged
def post_edit(request, post_id):
    post = Posts.objects.get(id=post_id)
    if request.method == 'GET':
        edit_form = ChangePostForm(instance=post)
        context = {
            'form': edit_form,
            'categories': categories,
            'post_id': post_id,
            'user_id': request.session.get('user')
        }
        return render(request, 'main_app/post_edit.html', context=context)
    elif request.method == 'POST':
        edit_form = ChangePostForm(request.POST, instance=post)
        if edit_form.is_valid():
            data = edit_form.cleaned_data

            if asyncio.run(main_check_profanity(data['title'], data['content'])):
                messages.error(request, 'Post contains obscene language.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            try:
                edit_form.save()
            except DatabaseError:
                messages.error(request, 'Something went wrong. Try again later.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Post was updated!')
                return HttpResponseRedirect(reverse('show_post', kwargs={'post_id': post_id}))
        else:
            messages.error(request, 'The fields must be filled according to filling rules.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Method not allowed.')


@is_logged
def post_delete(request, post_id):
    try:
        Posts.objects.get(id=post_id).delete()
    except Posts.DoesNotExist:
        return HttpResponseNotFound('Post does not exist.')
    else:
        return HttpResponseRedirect(reverse('posts'))


@is_logged
def add_like(request, post_id):
    post = Posts.objects.get(id=post_id)
    user = UserModel.objects.get(id=request.session.get('user'))
    if request.method == 'GET':
        try:
            post.likes_set.get(author=user)
        except Likes.DoesNotExist:
            post.likes_set.create(author=user)
        else:
            Likes.objects.filter(post=post, author=user).delete()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseBadRequest('Method not allowed.')


@is_logged
def add_dislike(request, post_id):
    post = Posts.objects.get(id=post_id)
    user = UserModel.objects.get(id=request.session.get('user'))
    if request.method == 'GET':
        try:
            post.dislikes_set.get(author=user)
        except Dislikes.DoesNotExist:
            post.dislikes_set.create(author=user)
        else:
            Dislikes.objects.filter(post=post, author=user).delete()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseBadRequest('Method not allowed.')


@is_logged
def add_comment(request, post_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():

            if asyncio.run(main_check_profanity(request.POST.get('content'))):
                messages.error(request, 'Your comment contains obscene language.')
                return HttpResponseRedirect(reverse('show_post', kwargs={'post_id': post_id}))

            response = comment_form.save_comment(request.session.get('user'), post_id)

            if response[1] == 200:
                messages.success(request, response[0])
            else:
                messages.error(request, response[0])
            return HttpResponseRedirect(reverse('show_post', kwargs={'post_id': post_id}))
        else:
            messages.error(request, 'The fields must be filled according to filling rules')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest('Method not allowed.')


@is_logged
def delete_comment(request, post_id, comment_id):
    Comments.objects.filter(id=comment_id).delete()
    return HttpResponseRedirect(reverse('show_post', kwargs={'post_id': post_id}))


@is_logged
def logout(request):
    del request.session['user']
    del request.session['is_authenticated']
    return HttpResponseRedirect('/users/signin/')
