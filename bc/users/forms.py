from disposable_email_domains import blocklist
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.urls import reverse

from .utils.email import EmailType, emails


class ConfirmedEmailAuthenticationForm(AuthenticationForm):
    """
    Tweak the AuthenticationForm class to  ensure that only users with
    confirmed email addresses can log in.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
        """Make sure the user is active and has a confirmed email address

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:  # type: ignore
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

        if not user.email_confirmed:  # type: ignore
            raise forms.ValidationError(
                "Please validate your email address to log in."
            )
