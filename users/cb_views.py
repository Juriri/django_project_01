from django.contrib.auth import authenticate, login
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.views.generic import CreateView, FormView

from utils.email import send_verification_email
from .forms import SignupForm, LoginForm
from .models import User


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_verification_email(self.request, user)
        return render(self.request, "registration/signup.html")

class LoginView(FormView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return render(self.request, 'registration/login.html', {
                'form': form,
                'error': '로그인 정보가 정확하지 않거나 이메일 인증이 필요합니다.'
            })

def verify_email(request):
    code = request.GET.get('code')
    signer = TimestampSigner()
    try:
        email = force_str(signer.unsign(code, max_age=60 * 60 * 24))  # 24시간 유효
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return render(request, 'registration/verify_success.html')
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return render(request, 'registration/verify_failed.html')
