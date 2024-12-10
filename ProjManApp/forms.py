from django import forms
from .models import User  # Import your custom User model

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['email', 'password']  # Exclude 'role' from the form fields if it's not user-provided

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default role to "Manager"
        self.instance.role = "Manager"  

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"]) 
        
        if commit:
            user.save()
        return user
