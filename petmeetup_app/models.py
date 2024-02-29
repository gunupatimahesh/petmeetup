from django.contrib.auth.models import User
from django.db import models

from petmeetup_app.utils import crop_square_image

# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not mobile:
            raise ValueError('The Mobile field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, mobile, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField()
    address = models.TextField()
    proof_id_card_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='user_images/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    pet_breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    available_for_meet_up = models.BooleanField(default=False)
    need_meet_up = models.BooleanField(default=False)
    need_day_care = models.BooleanField(default=False)
    day_care_available = models.BooleanField(default=False)
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
    breed_certificate = models.ImageField(upload_to='pet_certificates', null=True, blank=True)

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


class PetAvailableForDayCare(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    pet_breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_pet_type_display()} - {self.get_breed_display()} for {self.user.username}"


class PetNeedDayCare(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    pet_breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    size = models.CharField(max_length=10)
    vaccination_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_pet_type_display()} - {self.get_breed_display()} - {self.name} for {self.user.username}"
