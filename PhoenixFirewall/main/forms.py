from django import forms

class SecurityConfUpload(forms.Form):
    # define a form field for file upload
    file = forms.FileField()