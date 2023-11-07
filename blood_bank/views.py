# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from .forms import BloodBankRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from . import forms
from .forms import BloodBankUpdateForm
from users.models import BloodDonationRequest, Profile
from . import models
from .models import BloodBank, BloodInventory
from django.shortcuts import render, get_object_or_404
from django.http import Http404

def register_blood_bank(request):
    bbuserForm = forms.BloodBankUserForm()
    bbForm = forms.BloodBankForm()
    dict = {'bbuserForm':bbuserForm, 'bbForm': bbForm }
    if request.method == 'POST':
        bbuserForm = forms.BloodBankUserForm(request.POST)
        bbForm = forms.BloodBankForm(request.POST)
        if bbuserForm.is_valid() and bbForm.is_valid():
            user = bbuserForm.save()
            user.set_password(user.password)
            user.save()
            bb = bbForm.save(commit=False)
            
            bb.bloodbankUsername = user
            bb.save()
            blood_bank_group = Group.objects.get_or_create(name='BLOOD_BANK')
            blood_bank_group[0].user_set.add(user)
            username = bbuserForm.cleaned_data.get('username')
            
            messages.success(request, f'Account created for {username}!')
            return redirect('login_b')
    return render(request, 'blood_bank/register.html', context = dict )

def custom_login_bb(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            blood_bank = BloodBank.objects.get(bloodbankUsername = user)
            return redirect('profile_b')  
    else:
        form = AuthenticationForm()

    return render(request, 'blood_bank/login.html', {'form': form})

@login_required

@login_required
def bloodbank_update(request):
    bloodbank = BloodBank.objects.get(bloodbankUsername = request.user)

    if request.method == 'POST':
        form = BloodBankUpdateForm(request.POST, instance=bloodbank)
        if form.is_valid(): 
            form.save()
            return redirect('/bloodbank/profile/')

    else:
        form = BloodBankUpdateForm(instance=bloodbank)

    return render(request, 'blood_bank/bloodbank_update.html', {'form': form, 'bloodbank': bloodbank})
@login_required
def blood_bank_profile(request):
    blood_bank = models.BloodBank.objects.get(bloodbankUsername = request.user)
    return render (request, 'blood_bank/profile.html',{'blood_bank':blood_bank})

@login_required
def blood_bank_delete(request):
    if request.method == 'POST':
        user = request.user
        profile = BloodBank.objects.get(bloodbankUsername=user)
        profile.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('homepg')  
    return render(request, 'blood_bank/delete_account.html')

    
@login_required
def blood_inventory_view(request):
    blood_bank = BloodBank.objects.get(bloodbankUsername=request.user)
    # blood_inventory = BloodInventory.objects.filter(blood_bank=blood_bank)

    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_inventory = []

    for group in blood_groups:
        try:
            inventory = BloodInventory.objects.get(blood_bank=blood_bank, blood_group=group)
            blood_inventory.append(inventory)
        except BloodInventory.DoesNotExist:
            inventory = BloodInventory(blood_bank=blood_bank, blood_group=group, quantity=0)
            inventory.save()
            blood_inventory.append(inventory)

    context = {
        'blood_bank': blood_bank,
        'blood_inventory': blood_inventory
    }

    return render(request, 'blood_bank/bloodbank_dashboard.html', context)
@login_required
def blood_bank_dashboard(request):
    blood_bank = BloodBank.objects.get(bloodbankUsername=request.user)
    donation_requests = BloodDonationRequest.objects.filter(blood_bank=blood_bank)
    
    
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if action == 'accept':
            
            donation_request = BloodDonationRequest.objects.get(pk=request_id)
            donation_request.status = 'Accepted'
            donation_request.save()
            userl = donation_request.user  
            profile = Profile.objects.get(user=userl)
            blood_group = profile.blood_group
            inventory,created = BloodInventory.objects.get_or_create(blood_bank=blood_bank, blood_group=blood_group)
            inventory.quantity += 1
            profile.credits += 1
            inventory.save()
            profile.save()
            
        elif action == 'reject':
            donation_request = BloodDonationRequest.objects.get(pk=request_id)
            donation_request.status = 'Rejected'
            donation_request.save()
            
        return redirect('blood_bank_dashboard')
    
    return render(request, 'blood_bank/pending_requests.html', {'blood_bank': blood_bank, 'donation_requests': donation_requests})