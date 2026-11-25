from django.contrib import admin
from .models import Appointment

@admin.action(description="make them, AppointmentAdminPers")
def confirmed_appointment(admin.ModelAdmin):
    queryset.update(status='CONFIRMED')


@admin.register(Appointment)
class AppointmentAdminPers(admin.ModelAdmin):
    actions=[confirmed_appointment]
    list_display = ("reason", "status", "duration_minutes", "appointment_date")
    list_filter = ("status", "appointment_date")
    list_editable = ("status",)
    search_fields=("reason","status")
    ordering=("appointment_date",)
    fieldsets=(
        ('Description',{
            'fields':("reason","status","prescription")
        }),
        ("Date + Duration",{
            'fields':("appointment_date","duration_minutes")
        }),
        ("Planification",{
            'fields':("ceated_at","updated_at")
        }),
    )
    readonly_fields=("ceated_at","updated_at")


admin.site.register(Appointment, AppointmentAdminPers)