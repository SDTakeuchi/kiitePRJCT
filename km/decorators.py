#restricting access to certain pages depending on the user's status---------------------

from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *arg, **kwargs):
        if request.user.is_authenticated:
            return redirect('postIndex')
        else:
            return view_func(request, *arg, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *arg, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *arg, **kwargs)
            else:
                return HttpResponse('アクセス権限がありません。ブラウザから戻ってください。')
        return wrapper_func
    return decorator
    
def poster_only(view_func):
    def wrapper_func(request, *arg, **kwargs):
        if Post.user == request.user:
            return view_func(request, *arg, **kwargs)
        else:
            return redirect('postIndex')
    
    return wrapper_func