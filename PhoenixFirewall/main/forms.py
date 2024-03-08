from django import forms  
class SecurityConfUpload(forms.Form):  
    file = forms.FileField()