from django.urls import resolve
from django.shortcuts import redirect


class AuthenticationStatusMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        if request.user.is_authenticated:
            if url_name == "login_view" or url_name == "signup_view":
                return redirect("djangoadmin:account_view")
        elif not request.user.is_authenticated:
            if url_name == "logout_view":
                return redirect("djangoadmin:login_view")
        response = self.get_response(request)
        return response