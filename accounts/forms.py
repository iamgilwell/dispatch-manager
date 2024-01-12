from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import Group,Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from .models import UserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Button,
    ButtonHolder,
    Column,
    Div,
    Fieldset,
    Layout,
    Row,
    Submit,
    Field,
)
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
    validate_password,
)

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Email Address"}
        ),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form_control", "placeholder": "Enter your Password"}
        ),
    )


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=60,
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "form_control", "placeholder": "First name"}
        ),
    )
    last_name = forms.CharField(
        max_length=60,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "form_control", "placeholder": "Last name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form_control", "placeholder": "Enter your email here"}
        ),
    )
    password = forms.CharField(
        max_length=255,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form_control", "placeholder": "Enter password"}
        ),
    )

    password = forms.CharField(
        max_length=255,
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form_control", "placeholder": "Confirm Password"}
        ),
    )

    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(
            attrs={"class": "form_control", "placeholder": "Phone Number"}
        ),
        required=False,
    )

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "phone")

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            # return confirm_password
            msg = "Password and Confirm Passwords,do not match"
            # self.add_error('', msg)
            raise forms.ValidationError(msg)
            return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user_exist = User.objects.get(email__iexact=email)
            if user_exist:
                msg = "Email Address already exists"
                self.add_error("", msg)
                # raise forms.ValidationError(msg)
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.active = False
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two passwords entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    # password = ReadOnlyPasswordHashField()
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            'using <a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "active",
            "staff",
            "admin",
        )

    def clean_password(self):
        return self.initial["password"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("password", "active", "admin")

    # def clean_password(self):
    #     return self.initial["password"]


class ConfirmPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("password",)

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        password = cleaned_data.get("password")


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "state",
            "zip_code",
        ]


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        confirm_password = self.cleaned_data["current_password"]
        print(
            "[PasswordForm clean_current_password]  ------> make_password:   {}  ".format(
                confirm_password
            )
        )
        # If the user entered the current password, make sure it's right
        if self.cleaned_data["current_password"] and not self.user.check_password(
            self.cleaned_data["current_password"]
        ):
            raise ValidationError(
                "This is not your current password. Please try again."
            )

        # If the user entered the current password, make sure they entered the new passwords as well
        if self.cleaned_data["current_password"] and not (
            self.cleaned_data["password"] or self.cleaned_data["confirm_password"]
        ):
            raise ValidationError(
                "Please enter a new password and a confirmation to update."
            )

        return self.cleaned_data["current_password"]

    def clean_confirm_password(self):
        # Make sure the new password and confirmation match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")

        if password1 != password2:
            raise forms.ValidationError(
                "Your passwords didn't match. Please try again."
            )

        return self.cleaned_data.get("confirm_password")


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        error_messages={"required": "First Name is a required field"},
        required=True,
    )
    last_name = forms.CharField(
        max_length=100,
        error_messages={"required": "Last Name is a required field"},
        required=True,
    )
    email = forms.EmailField(
        max_length=254,
        error_messages={"required": "Email Address is a required field"},
        help_text="e.g youremail@makeup.com",
    )
    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(
            attrs={"class": "form_control", "placeholder": "Phone Number"}
        ),
        error_messages={"required": "Phone Number is a required field"},
        required=True,
    )
    staff_id = forms.CharField(
        max_length=100,
        error_messages={"required": "Staff ID is a required field"},
        required=True,
    )
    role = forms.ChoiceField(
        required=True,
        choices=User.ROLE_CHOICES,
    )
    
    bio = forms.CharField(max_length=20000, required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

    # def clean(self):
    #  if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
    #         raise ValidationError({'email': _('Email already exists.')})

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "staff_id",
            "role",
            "bio",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already exists in the system")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone Already exists in the system")
        return phone


class UpdateUserForm(forms.ModelForm):
    # admin
    # staff
    # active

    first_name = forms.CharField(
        max_length=100,
        error_messages={"required": "First Name is a required field"},
        required=True,
    )
    last_name = forms.CharField(
        max_length=100,
        error_messages={"required": "Last Name is a required field"},
        required=True,
    )
    email = forms.EmailField(
        max_length=254,
        error_messages={"required": "Email Address is a required field"},
        help_text="e.g youremail@makeup.com",
    )
    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(
            attrs={"class": "form_control", "placeholder": "Phone Number"}
        ),
        error_messages={"required": "Phone Number is a required field"},
        required=True,
    )
    staff_id = forms.CharField(
        max_length=100,
        error_messages={"required": "Staff ID is a required field"},
        required=True,
    )
    role = forms.ChoiceField(
        required=True,
        choices=User.ROLE_CHOICES,
        error_messages={"required": "Role is a required field"},
    )
    
    bio = forms.CharField(max_length=20000, required=False)

    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

    def clean(self):
     if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('Email already exists.')})

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "staff_id",
            "role",
            "bio",
            "password",
        )


class ActivateChangePassword(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("password",)