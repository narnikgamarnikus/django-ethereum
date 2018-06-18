from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class PayForm(forms.Form):

    value = forms.DecimalField(decimal_places=10)
    gas = forms.PositiveIntegerField()
    address = forms.CharField()

    def clean_address(self):
        address = self.cleaned_data['address']
        if not address.startswith('0x'):
            raise ValidationError(_('First two symbols of address must be 0x'))
        return address

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
