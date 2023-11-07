from django.contrib import admin

# Register your models here.
from .models import Profile,BloodDonationRequest
admin.site.register(BloodDonationRequest)
admin.site.register(Profile)
