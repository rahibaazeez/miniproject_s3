from django.core.management.base import BaseCommand
from user.models import Appointment
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send reminder emails to employees 3 days before the event'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        reminder_date = today + timedelta(days=3)
        # Query confirmed appointments happening 3 days from now
        appointments = Appointment.objects.filter(status='Confirmed', event__event_date=reminder_date)
        
        for appointment in appointments:
            # Here, send email logic will go
            self.stdout.write(f"Reminder sent to {appointment.employee.email} for event {appointment.event.event_name}")
