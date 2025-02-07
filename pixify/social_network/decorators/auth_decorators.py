from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator


def auth_required(view_func):
    """
    Custom decorator to apply login_required to CBV methods.
    """
    return method_decorator(login_required)(view_func)


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return redirect('/request-otp')

            # Check if the user has any of the required roles
            if len(set(request.user.roles) & set(roles)) > 0:
                return view_func(self, request, *args, **kwargs)
            else:
                return render(request, "error/403.html")

        # If this is a method in a class-based view, apply as a method_decorator
        return (
            method_decorator(_wrapped_view, name="dispatch")
            if hasattr(view_func, "view_class")
            else _wrapped_view
        )

    return decorator

