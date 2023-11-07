from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, BloodDonationRequest
from blood_bank.models import BloodBank

class DonorUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DonorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','gender','contact_num','email_id','state','district','address','pincode','blood_group']

class BloodDonationRequestForm(forms.ModelForm):
    class Meta:
        model = BloodDonationRequest
        fields = ['blood_bank']
from django import forms

# Define choices for blood groups
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

class BloodRequestForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        label="Blood Group",
    )
    quantity = forms.IntegerField(
        label="Quantity (in mL)",
        min_value=1,  # Adjust the minimum quantity as needed
    )
    blood_bank = forms.ModelChoiceField(
        queryset=BloodBank.objects.all(),
        label="Select Blood Bank"
    )
