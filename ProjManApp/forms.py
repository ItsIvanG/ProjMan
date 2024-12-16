from django import forms
from .models import User  # Import your custom User model

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['email', 'password', 'username','name','profile_picture']  # Exclude 'role' from the form fields if it's not user-provided

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default role to "Manager"
        self.instance.role = "Manager"  

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        # user.email = self.cleaned_data["email"]
        # user.name = self.cleaned_data["name"]

        user.username = self.cleaned_data["username"]

        user.set_password(self.cleaned_data["password"]) 

        if commit:
            user.save()  # Save the user first to generate an ID
            user.manager = user  # Set the manager field to the user itself
            user.save()  # Save the user again after setting the manager
        
        return user