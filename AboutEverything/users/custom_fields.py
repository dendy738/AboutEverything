from django import forms
from django.core.validators import RegexValidator


class PhoneWidget(forms.MultiWidget):
    def __init__(self, choices=(), attrs=None):
        widgets = {
            'code': forms.Select(choices=choices, attrs={'class': 'multi-widget'}),
            'number': forms.TextInput(attrs={'class': 'multi-widget'}),
        }
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, str):
            if '|' in value:
                return value.split('|')
            else:
                return ['', '']
        return ['', '']



class PhoneField(forms.MultiValueField):
    widget = PhoneWidget

    def __init__(self, **kwargs):
        fields = [
            forms.CharField(max_length=15),
            forms.CharField(max_length=20, validators=[RegexValidator(regex=r'[0-9]+', message='Phone number must contain only digits.')])
        ]
        super().__init__(fields, **kwargs)


    def compress(self, data_list):
        if data_list:
            return '|'.join(data_list)
        return ''

