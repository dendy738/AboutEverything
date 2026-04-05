from django.http import HttpResponseRedirect
from functools import wraps


def is_logged(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if view.__name__ == 'user_auth':
            if 'user' not in request.session or not request.session.get('is_authenticated', False):
                return view(request, *args, **kwargs)
            return HttpResponseRedirect('/posts')
        else:
            if 'user' not in request.session or not request.session.get('is_authenticated', False):
                return HttpResponseRedirect('/users/signin/')
            return view(request, *args, **kwargs)
    return wrapper
