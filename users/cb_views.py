from django.contrib.auth import authenticate, login
from django.core import signing
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.views.generic import CreateView, FormView

from utils.email import send_verification_email
from .forms import SignupForm, LoginForm
from .models import User


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        print("==== 이메일 인증 링크 확인용 ====")
        user = form.save()
        # 인증 메일 발송
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        url = f"{self.request.scheme:}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}"
        subject = f"[Todo]{user.email}님의 이메일 인증 링크입니다."
        message = f"""
            아래의 링크를 클릭하여 이메일 인증을 완료해주세요.\n\n
            {url}
            """
        print("==== 이메일 인증 링크 확인용 ====")
        print("signed_email:", signed_user_email)
        print("dumps된 인증코드:", signer_dump)
        print("최종 인증 URL:", url)
        print("================================")
        send_verification_email(subject=subject, message=message, from_email=None, to_email=user.email)

        return render(
            request=self.request,
            template_name="registration/signup_done.html",
            context={
                'user': user,
            }
        )

def verify_email(request):
    code = request.GET.get('code', '')

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        user_email = signer.unsign(decoded_user_email, max_age=60 * 5)
    except (TypeError, SignatureExpired):
        return render(request, 'registration/verify_failed.html')

    user = get_object_or_404(User, email=user_email)
    user.is_active = True
    user.save()
    return render(request, 'registration/verify_success.html')

class LoginView(FormView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("cbv_todo_list")

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