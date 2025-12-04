from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
# class UserProfile(AbstractUser):
#     photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     address = models.TextField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username