from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import BadHeaderError, HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm

from .forms import SignupForm
from .tokens import account_activation_token
from item.models import Cartegory, Item

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .forms import PasswordResetForm, SetNewPasswordForm

def sold(request):
    items = Item.objects.filter(is_sold=True)[:20]
    cartegories = Cartegory.objects.all()
    return render(request, 'core/sold.html', {
        'cartegories': cartegories,
        'items': items,
    })
def index(request):
     return render(request, 'core/index.html')

def index1(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')
    cartegories = Cartegory.objects.all()
    return render(request, 'core/index1.html', {
        'cartegories': cartegories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def auth_view(request):
    login_form = AuthenticationForm()
    signup_form = SignupForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    return redirect('core:index1')
        elif 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = False  # Deactivate account until it is confirmed
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your Account'
                message = render_to_string('core/account_activation_email.html', {
                    'user': user,
                    'domain': '127.0.0.1:8000',  # Local development domain
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(subject, message, 'otiecollins131@gmail.com', [user.email], fail_silently=False)
                return redirect('core:account_activation_sent')

    return render(request, 'core/auth.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('core:index1')
    else:
        return render(request, 'core/activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'core/account_activation_sent.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'core/password_reset.html'
    form_class = PasswordResetForm
    email_template_name = 'core/password_reset_email.html'
    success_url = reverse_lazy('core:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'core/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('core:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'core/password_reset_complete.html'

def logout_view(request):
    logout(request)
    return redirect('/index1')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_of_use(request):
    return render(request, 'core/terms_of_use.html')

def faq(request):
    return render(request, 'core/faq.html')

def about(request):
    return render(request, 'core/about.html')
