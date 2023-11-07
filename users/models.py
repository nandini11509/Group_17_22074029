from django.db import models
from django.contrib.auth.models import User
from blood_bank.models import BloodBank
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    contact_num = models.CharField(max_length=15)
    email_id = models.EmailField()
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    credits = models.IntegerField(default=0)
    blood_group = models.CharField(max_length=3, choices=(
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ))

class BloodDonationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')),default="Pending")
    request_date = models.DateTimeField(auto_now_add=True)
    date=models.DateField(auto_now=True)