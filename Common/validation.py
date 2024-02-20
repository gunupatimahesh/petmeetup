from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from petmeetup_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # ... other fields and methods ...

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    # def clean_mobile(self):
    #     mobile = self.cleaned_data.get('mobile')
    #     # Implement your mobile validation logic here
    #     return mobile
