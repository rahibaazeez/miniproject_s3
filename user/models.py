from django.db import models
from django.utils import timezone

class Login(models.Model):
    username = models.EmailField(unique=True)  # this will be the email
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.username



class Register(models.Model):
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    aadhaar_number = models.CharField(max_length=14, unique=True)
    aadhaar_file = models.FileField(upload_to="aadhaar_files/", null=True, blank=True)
    photo = models.ImageField(upload_to="uploads/", null=True, blank=True)
    login = models.OneToOneField(Login, on_delete=models.CASCADE, null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)


    def __str__(self):
        return self.full_name


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("Birthday", "Birthday"),
        ("Marriage", "Marriage"),
        ("Engagement", "Engagement"),
        ("Festival", "Festival"),
        ("Corporate", "Corporate"),
        ("Other", "Other"),
    ]

    PLACE_CHOICES = [
        ("Convention Center", "Convention Center"),
        ("Hall", "Hall"),
        ("Destination", "Destination"),
        ("Home", "Home"),
        ("Outdoor Ground", "Outdoor Ground"),
    ]

    event_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    place_type = models.CharField(max_length=50, choices=PLACE_CHOICES)
    event_date = models.DateField()
    event_time = models.TimeField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    vacancy = models.IntegerField(default=0)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event_name} - {self.event_date}"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Confirmed", "Confirmed"),
        ("Declined", "Declined"),
        ("Cant Attend", "Cant Attend"),  # NEW STATUS
    ]

    employee = models.ForeignKey(Register, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Applied")

    class Meta:
        unique_together = ('employee', 'event')

    def __str__(self):
        return f"{self.employee.full_name} - {self.event.event_name} ({self.status})"
