from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=200)
    phone_code = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class UserModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80)
    second_last_name = models.CharField(max_length=80, null=True, blank=True)
    birthday = models.DateField()
    user_name = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=25, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)

