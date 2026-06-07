import secrets
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import RegistrationForm, LoginForm
from .models import UserProfile
from .email_utils import send_welcome_email

logger = logging.getLogger('accounts')


def home(request):
    """
    Landing page: shows login and registration tabs.
    Redirects to dashboard if user is already logged in.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm()
    login_form = LoginForm()

    return render(request, 'index.html', {
        'form': form,
        'login_form': login_form,
    })


def register_view(request):
    """
    Handle registration form submission.

    Flow:
    1. Validate form fields + captcha
    2. Check email uniqueness (in form's clean_email)
    3. Generate a secure random password
    4. Create Django User (email as username)
    5. Create UserProfile linked to User
    6. Send welcome email with credentials
    7. Redirect to success page (never shows password)
    """
    if request.method != 'POST':
        return redirect('home')

    form = RegistrationForm(request.POST)

    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']

        # Generate a secure random password (~16 characters)
        generated_password = secrets.token_urlsafe(12)
        logger.info(f"[PASSWORD_GENERATED] Secure password generated for {email}")

        # Create Django User with email as username
        user = User.objects.create_user(
            username=email,
            email=email,
            password=generated_password,
            first_name=first_name,
            last_name=last_name,
        )

        # Create linked UserProfile
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        logger.info(f"[REGISTRATION] Account created for {email} (User ID: {user.id})")

        # Send welcome email with credentials (plain text + HTML)
        email_sent = send_welcome_email(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generated_password,
        )

        # Always show success page — never display generated password
        return render(request, 'success.html', {
            'email': email,
            'email_sent': email_sent,
        })

    else:
        # Form invalid (captcha failed, email exists, etc.)
        logger.warning(f"[REGISTRATION_FAILED] Form errors: {form.errors.as_text()}")
        login_form = LoginForm()
        return render(request, 'index.html', {
            'form': form,
            'login_form': login_form,
            'show_register': True,
        })


def login_view(request):
    """
    Handle login form submission.

    Flow:
    1. Validate email + password fields
    2. Authenticate using email as username
    3. Create session and redirect to dashboard
    4. On failure: show clear error message
    """
    if request.method != 'POST':
        return redirect('home')

    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        email = login_form.cleaned_data['email']
        password = login_form.cleaned_data['password']

        # Django authenticate using email as username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"[LOGIN_SUCCESS] Successful login for {email}")
            return redirect('dashboard')
        else:
            # Check if user exists at all to give a better error message
            user_exists = User.objects.filter(username=email).exists()
            if user_exists:
                error_msg = 'Incorrect password. Please try again.'
            else:
                error_msg = 'No account found with this email. Please create an account first.'

            logger.warning(f"[LOGIN_FAILED] Failed login attempt for {email} (user exists: {user_exists})")
            form = RegistrationForm()
            return render(request, 'index.html', {
                'form': form,
                'login_form': login_form,
                'login_error': error_msg,
            })
    else:
        logger.warning(f"[LOGIN_FAILED] Form validation errors: {login_form.errors.as_text()}")
        form = RegistrationForm()
        return render(request, 'index.html', {
            'form': form,
            'login_form': login_form,
            'login_error': 'Please enter a valid email address and password.',
        })


@login_required
@never_cache
def dashboard_view(request):
    """
    Dashboard page — only accessible after successful login.
    Uses Django session authentication via @login_required.
    @never_cache prevents browser from caching — back button won't show
    dashboard after logout.
    """
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()

    # Build display data from profile or fallback to User model
    if profile:
        full_name = f"{profile.first_name} {profile.last_name}"
        email = profile.email
        initials = (profile.first_name[0] + profile.last_name[0]).upper()
    else:
        full_name = user.get_full_name() or user.username
        email = user.email or user.username
        initials = full_name[:2].upper() if full_name else 'U'

    return render(request, 'dashboard.html', {
        'full_name': full_name,
        'email': email,
        'initials': initials,
    })


@require_POST
def logout_view(request):
    """
    Log the user out, flush the session completely, and redirect.
    @require_POST ensures logout cannot happen via GET (CSRF protection).
    session.flush() destroys all session data so back button can't reopen.
    """
    if request.user.is_authenticated:
        logger.info(f"[LOGOUT] User {request.user.username} logged out")
    request.session.flush()
    logout(request)
    return redirect('home')


def success_view(request):
    """
    Registration success page fallback.
    Only used if someone navigates to /success/ directly.
    """
    return redirect('home')


def csrf_failure_view(request, reason=''):
    """
    Custom CSRF failure page.
    Shows a user-friendly message instead of Django's raw Forbidden (403).
    """
    return render(request, 'csrf_failure.html', status=403)


def custom_404_view(request, exception):
    """Custom 404 page."""
    return render(request, 'errors/404.html', status=404)


def custom_500_view(request):
    """Custom 500 page."""
    return render(request, 'errors/500.html', status=500)