from django.contrib import admin

# Register your models here.
from .models import BloodBank,BloodInventory,BloodRequest
admin.site.register(BloodInventory)
admin.site.register(BloodBank)
admin.site.register(BloodRequest)