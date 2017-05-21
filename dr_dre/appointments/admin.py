from django.contrib import admin

from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time_start', 'time_end', 'visitor', 
                    'non_recurring', 'reason')
    list_filter = ('date', )
    list_select_related = ('visitor', )
    search_fields = ('visitor', 'non_recurring', 'reason')
