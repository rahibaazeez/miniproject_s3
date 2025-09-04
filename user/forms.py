from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'id': 'password',
            'required': True
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'id': 'confirmPassword',
            'required': True
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Register
        fields = ['full_name', 'dob', 'email', 'phone', 'aadhaar_number', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'id': 'fullName',
                'required': True
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
                'id': 'dob',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'name@example.com',
                'id': 'email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'pattern': '[0-9]{10}',
                'placeholder': '1234567890',
                'title': 'Enter 10‑digit number',
                'id': 'phone',
                'required': True
            }),
            'aadhaar_number': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '14',
                'placeholder': 'xxxx xxxx xxxx',
                'id': 'aadhaar',
                'required': True
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-sm',
                'accept': 'image/*',
                'id': 'photo',
                'required': True
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
