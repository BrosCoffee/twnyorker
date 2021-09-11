from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import SiteUser

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'email', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'   ].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'    ].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'        ].widget.attrs['placeholder'] = 'Email'
        self.fields['date_of_birth'].widget.attrs['placeholder'] = 'Date of Birth (MM/DD/YYYY)'
        self.fields['password1'    ].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'    ].widget.attrs['placeholder'] = 'Confirm Password'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserSignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserSignInForm, self).__init__(*args, **kwargs)
        self.fields['email'   ].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    def clean_email(self):
        return self.cleaned_data['email'].lower()

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'   ].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'    ].widget.attrs['placeholder'] = 'Last Name'
        # self.fields['email'        ].widget.attrs['placeholder'] = 'Email'
        # self.fields['email'        ].widget.attrs['readonly'] = True
        self.fields['date_of_birth'].widget.attrs['placeholder'] = 'Date of Birth (MM/DD/YYYY)'
        self.fields['password1'    ].widget.attrs['placeholder'] = 'New Password'
        self.fields['password2'    ].widget.attrs['placeholder'] = 'Confirm New Password'