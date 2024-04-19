from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name','email', 'password1','password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[-1]
        allowed_domains = ['nmamit.in', 'nitte.edu.in']

        if domain not in allowed_domains:
            raise forms.ValidationError("Only nmamit.in or nitte.edu.in emails are allowed.")
        return email
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        # Set is_staff field based on the email domain
        if user.email.endswith('nitte.edu.in'):
            user.is_staff = True

        if commit:
            user.save()
        
        return user
class UploadFileForm(forms.Form):
    file = forms.FileField()