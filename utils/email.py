from django.core.signing import TimestampSigner
from django.core.signing import TimestampSigner
from django.conf import settings

def send_verification_email(request, user):
    signer = TimestampSigner()
    signed_code = signer.sign(user.email)
    verify_url = request.build_absolute_uri(f"/users/verify-email/?code={signed_code}")

    subject = "[MyTodoApp] 이메일 인증을 완료해주세요"
    message = f"아래 링크를 클릭하여 회원가입을 완료하세요:\n\n{verify_url}"
    from config import settings
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
