from django.db import models
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

class BloodBank(models.Model):
    bloodbankUsername = models.OneToOneField(User, on_delete=models.CASCADE )
    bloodbankName = models.CharField(max_length=100)
    Address = models.CharField(max_length=200)
    City = models.CharField(max_length=100)
    ContactNumber = models.CharField(max_length=13)
    emailID = models.EmailField(max_length=100)
    def __str__(self):
        return self.bloodbankName

    # class Meta:
    #     app_label = 'blood_bank'
# Create your models here.
class BloodInventory(models.Model):
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=(
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ))
    quantity = models.IntegerField(default = 0)

class BloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=(
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ))
    quantity = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(
        ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')
    ), default="Pending")

