from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import SignupForm
from .tokens import account_activation_token

# Create your views here.
def view(request, username):
    users = User.objects.get(username=username)
    return render(request, 'userprofile/view.html', {'users': users})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = render_to_string('userprofile/acc_active_email.html', {
                'user':user, 
                'request':request,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            subject = 'Please activate your demokratia.my account'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address.')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return HttpResponse('Account activated successfully')
    else:
        return render(request, 'registration/account_activation_invalid.html')
