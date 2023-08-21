from django import forms
from .models import User
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    class Meta:
        # db_table = User
        model = User
        fields = ('password', 'confirm_password', 'first_name', 'last_name','username','email')
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
    
    