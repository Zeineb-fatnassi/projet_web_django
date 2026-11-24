from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Le numéro doit contenir exactement 8 chiffres.",
)


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à la date du jour.")


class Specialty(models.Model):
    name = models.CharField('Nom', max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    pass


class Doctor(User):
    license_number = models.CharField(
        "N° d'inscription à l'ordre",
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)],
    )
    phone = models.CharField('Téléphone', max_length=8, validators=[phone_validator])
    specialties = models.ManyToManyField(Specialty, related_name='doctors')

    def __str__(self):
        return f"Dr {self.last_name} {self.first_name}"


class Patient(User):
    national_id = models.CharField(
        'CIN',
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$', "Le CIN doit contenir exactement 8 chiffres.")],
    )
    phone = models.CharField('Téléphone', max_length=8, validators=[phone_validator])
    birth_date = models.DateField('Date de naissance', validators=[validate_past_date])

    def __str__(self):
        return f"{self.last_name} {self.first_name}"