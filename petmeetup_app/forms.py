from django import forms

from petmeetup_app.models import PetMeetUp


class PetMeetUpForm(forms.ModelForm):
    class Meta:
        model = PetMeetUp
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PetMeetUpForm, self).__init__(*args, **kwargs)
        self.fields['pet_image'].widget.attrs.update({'class': 'form-control'})

