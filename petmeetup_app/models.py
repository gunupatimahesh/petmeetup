from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from petmeetup_app.utils import crop_square_image


class PetType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PetBreed(models.Model):
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PetMeetUp(models.Model):
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    pet_breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    available_for_meet_up = models.BooleanField(default=False)
    need_meet_up = models.BooleanField(default=False)
    need_day_care = models.BooleanField(default=False)
    pet_description = models.TextField()

    # Additional Attributes
    size = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')],
                              default='unknown')
    coat_length = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    good_with = models.CharField(max_length=50, blank=True, null=True)
    care_and_behavior = models.TextField(blank=True, null=True)
    days_of_pet_finder = models.PositiveIntegerField(blank=True, null=True)
    shelter_or_rescue = models.CharField(max_length=100, blank=True, null=True)
    pet_image = models.ImageField(upload_to='pet_images/', null=True, blank=True)

    # ... other fields

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pet_image:
            # Get the path of the uploaded image
            image_path = self.pet_image.path

            # Crop and resize the image
            cropped_image = crop_square_image(image_path)

            # Save the cropped image back to the original path
            cropped_image.save(image_path, 'JPEG', quality=90)

    def __str__(self):
        return f"{self.pet_name} - {self.pet_type.name} - {self.pet_breed.name}"
