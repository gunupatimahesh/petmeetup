from django.contrib import admin
from .models import PetType, PetBreed, PetMeetUp

admin.site.register(PetType)
admin.site.register(PetBreed)
admin.site.register(PetMeetUp)
