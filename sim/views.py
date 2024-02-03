from django.http import HttpRequest
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.shortcuts import redirect
from django.contrib.auth import login
from .services import send_sign_in_email, decode_uid, get_user_by_uid
from .forms import CreateUserForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


def verify_email(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """
    Verify user email after the user clicks on the email link.
    """
    uid = decode_uid(uidb64)
    user = get_user_by_uid(uid) if uid else None

    if user and default_token_generator.check_token(user, token):
        user.has_verified_email = True
        user.save()
        login(request, user)
        return redirect('home')

    print("Email verification failed")
    return redirect('sign_in')


class SendSignInEmail(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_anonymous and request.user.has_verified_email:
            return redirect('home')
        form = CreateUserForm()
        return render(request, 'sign_in.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        data = {
            'username': request.POST['email'],
            'email': request.POST['email'],
            'password': request.POST['email']
        }
        user, created = User.objects.get_or_create(
            email=data['email'],
            defaults={'username': data['email'], 'password': data['email']}
        )
        return self._send_verification_and_respond(user)

    @staticmethod
    def _send_verification_and_respond(user: User) -> HttpResponse:
        send_sign_in_email(user)
        message = (
            f"We've sent an email ✉️ to "
            f'<a href=mailto:{user.email}" target="_blank">{user.email}</a> '
            "Please check your email to verify your account"
        )
        return HttpResponse(message)


def sign_out(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    return redirect('sign_in')


def home(request: HttpRequest) -> HttpResponse:
    if not request.user.is_anonymous and request.user.has_verified_email:
        return render(request, 'home.html')
    else:
        return redirect('sign_in')


