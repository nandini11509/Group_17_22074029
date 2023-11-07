from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BloodBank

# class BloodBankRegistrationForm(UserCreationForm):
#     bloodbankName = forms.CharField(max_length=100)
#     Address = forms.CharField(max_length=200)
#     City = forms.CharField(max_length=100)
#     ContactNumber = forms.CharField(max_length=13)
#     emailID = forms.EmailField(max_length=100)

#     class Meta:
#         model = User
#         fields = ['username','bloodbankName', 'Address', 'City', 'ContactNumber', 'emailID','password1','password2']

class BloodBankUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'password']
        widgets = {
        'password': forms.PasswordInput()
        }
class BloodBankForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        fields = ['bloodbankName','Address','City','ContactNumber','emailID']
class BloodBankUpdateForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        fields = ['bloodbankName', 'Address', 'City', 'ContactNumber', 'emailID']
