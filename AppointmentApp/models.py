from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    reason = models.TextField('Motif')
    prescription = models.FileField(
        'Ordonnance',
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    status = models.CharField(
        'Statut',
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    duration_minutes = models.PositiveIntegerField('Durée (min)', default=30)
    appointment_date = models.DateTimeField('Date du rendez-vous')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
    )

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unicite_patient_doctor_date',
                violation_error_message="ce docteur possède un rendez-vouz à cette date"
            )
        ]

    def clean(self):
        modified_date = self._state.adding or (
            Appointment.objects.filter (
                pk=self.pk,
                appointment_date=self.appointment_date
            ).exists()
        )
        if self.appointment_date<=timezone.now():
            raise ValidationError("la date rdv doit etre superieure à la date d'aujourd'hui")
        
        

    def __str__(self):
        return f"RDV {self.appointment_date:%d/%m/%Y %H:%M} - {self.doctor} / {self.patient}"