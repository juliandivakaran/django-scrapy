from django import forms

class URLinputForm(forms.Form):
    url = forms.URLField(label='URL', required=True)

