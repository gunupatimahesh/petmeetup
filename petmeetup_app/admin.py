from django.contrib import admin
from .models import PetType, PetBreed, PetMeetUp, PetNeedDayCare, PetAvailableForDayCare, CustomUser

admin.site.register(PetType)
admin.site.register(PetBreed)
admin.site.register(PetMeetUp)
admin.site.register(PetNeedDayCare)
admin.site.register(PetAvailableForDayCare)
admin.site.register(CustomUser)
