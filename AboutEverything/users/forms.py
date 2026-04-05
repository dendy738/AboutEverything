from django import forms
from .custom_fields import PhoneField
from .models import Country


MONTHS = {
    1: 'Jan', 2: 'Feb', 3: 'Mar',
    4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep',
    10: 'Oct', 11: 'Nov', 12: 'Dec'
}

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    second_last_name = forms.CharField(max_length=50, required=False, label="Second Last Name (optional)")
    birthday = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'my-date-select'}, years=range(1960, 2050), months=MONTHS), label="Your Birthday")
    user_name = forms.CharField(max_length=25, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, max_length=20, label="Password")
    repeat_pass = forms.CharField(widget=forms.PasswordInput, max_length=30, label='Repeat Password')
    email = forms.EmailField(label="Email")
    country = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'my-date-select'}), label='Country')
    contact_number = PhoneField(label="Contact Number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        countries = Country.objects.all()
        codes = []
        counts = []
        for c in countries:
            el1 = (c.phone_code, c.phone_code)
            el2 = (c.name, c.name)
            if el2 not in counts:
                counts.append(el2)
            codes.append(el1)

        self.fields['contact_number'].widget.widgets[0].choices = codes
        self.fields['country'].choices = counts


class UserAuthorizationForm(forms.Form):
    username = forms.CharField(max_length=80, label='Enter your username')
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label='Enter your password')


class UserEmailForm(forms.Form):
    email = forms.EmailField(label='Enter your email')


class UserNewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label='New password')
    repeat_pass = forms.CharField(widget=forms.PasswordInput, max_length=30, label='Repeat new password')