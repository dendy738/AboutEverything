from django import forms
from users.models import UserModel, Country
from users.forms import MONTHS
from users.custom_fields import PhoneField


class ProfileForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'my-date-select'}, years=range(1940, 2050), months=MONTHS), label='Birth Date')
    country = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'my-date-select'}), label='Country')
    contact_number = PhoneField()
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'second_last_name', 'birthday', 'user_name', 'email', 'country', 'contact_number')

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