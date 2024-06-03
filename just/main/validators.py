from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomSeekerPasswordValidator:
    def validate(self, password, user=None):
        if len(password) != 4 or not password.isdigit():
            raise ValidationError(
                _('Пароль має містити рівно 4 цифри для пошуковців.'),
                code='invalid_password',
            )

    def get_help_text(self):
        return _(
            "Пароль має містити рівно 4 цифри для пошуковців."
        )

class EmployerPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code='password_too_short',
            )
        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters and must not be entirely numeric."
        )