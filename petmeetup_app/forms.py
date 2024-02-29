from django import forms
from django.contrib.auth.forms import UserCreationForm

from petmeetup_app.models import PetMeetUp, CustomUser


class PetMeetUpForm(forms.ModelForm):
    class Meta:
        model = PetMeetUp
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PetMeetUpForm, self).__init__(*args, **kwargs)
        self.fields['pet_image'].widget.attrs.update({'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'address', 'proof_id_card_number',
                  'photo', 'password1', 'password2', 'age']
