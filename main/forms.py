from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django.forms.models import ALL_FIELDS
from .models import GDZS, CustomUser, Post, PassedApprovals, InitialTrainingPeriod
from django import forms
from django.core.exceptions import ValidationError
import unicodedata
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.forms import UserCreationForm  
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.text import capfirst
from betterforms.multiform import MultiModelForm

UserModel = get_user_model()


class EmailField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'email',
        }

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = CustomUser
        fields = ("email",)
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True



    def save(self, commit=True):
        user = super().save(commit=False)
        user.fullname = user.email
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'registration/widgets/read_only_password_hash.html'
    read_only = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("No password set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context

    def id_for_label(self, id_):
        return None

class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault('disabled', True)
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = '__all__'
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите действующие %(email)s и пароль. Оба поля чувствительны к регистру."
        ),
        'inactive': _("Этот аккаунт не активен"),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        email_max_length = self.username_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.username_field.verbose_name},
        )

class UserEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['fullname', 'post', 'rank', 'bdate', 'document']


class PassedApprovalsEditForm(ModelForm):
    class Meta:
        model = PassedApprovals
        fields = ['fullname','result', 'why', 'attdate', 'profdate', 'approvalsname']

class InitialTrainingPeriodEditForm(ModelForm):
    class Meta:
        model = InitialTrainingPeriod
        fields = ['fullname','start', 'end']

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['fullname','rtp', 'passdate']

class GDZSEditForm(ModelForm):
    class Meta:
        model=GDZS
        fields=['fullname','value','possible', 'why_not']

class UserEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserEditForm,
        'passedapprovals': PassedApprovalsEditForm,
        'period': InitialTrainingPeriodEditForm,
        'post': PostEditForm,
        'gdzs':GDZSEditForm
    }

    