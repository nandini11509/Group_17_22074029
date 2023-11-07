from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from blood_bank.models import BloodBank,BloodInventory
from django.contrib.auth.models import Group
from . import forms,models
from .models import Profile
from .forms import BloodDonationRequestForm,BloodRequestForm
from blood_bank.models import BloodRequest

def register(request):
    userForm = forms.DonorUserForm()
    donorForm = forms.DonorForm()
    mydict = {'userForm':userForm, 'donorForm': donorForm}
    if request.method == 'POST':
        userForm = forms.DonorUserForm(request.POST)
        donorForm = forms.DonorForm(request.POST, request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            donor = donorForm.save(commit=False)
            donor.user = user
            donor.blood_group = donorForm.cleaned_data['blood_group']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
            username = userForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login_users')
    
    return render(request, 'users/register.html', context=mydict)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/users/user_past_requests')  # Redirect to a custom URL after login
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_user(request):
    # return render(request, 'users/profile.html')
    user_profile = models.Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'user_profile': user_profile})

@login_required
def update_profile(request):
    profile = models.Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = forms.DonorForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_user')
    else:
        form = forms.DonorForm(instance=profile)
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        profile = models.Profile.objects.get(user=user)
        user.delete()
        profile.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('homepg')  # Redirect to your home page or any other appropriate URL
    return render(request, 'users/delete_account.html')
# views.py

# def profile_user(request):
    

def show_blood_banks(request):
    city = request.GET.get('City', '')  # Get the selected city from the request
    blood_banks = BloodBank.objects.filter(City=city)
    
    # Create a list to store blood bank details with inventory
    blood_bank_details = []
    
    for blood_bank in blood_banks:
        inventory = BloodInventory.objects.filter(blood_bank=blood_bank)
        blood_bank_details.append({'blood_bank': blood_bank, 'inventory': inventory})
    
    return render(request, 'users/showbb.html', {'blood_bank_details': blood_bank_details, 'blood_banks': blood_banks})

@login_required
def create_donation_request(request):
    if request.method == 'POST':
        form =  BloodDonationRequestForm(request.POST)
        if form.is_valid():
            donation_request = form.save(commit=False)
            donation_request.user = request.user  # Assuming the user is logged in
            donation_request.save()
            # profile = Profile.objects.get(user=request.user)
            # profile.credits += 1  # Add one credit for the successful donation
            # profile.save()
            return redirect('donation_success')  # Redirect to a success page
    else:
        form = BloodDonationRequestForm()

    return render(request, 'users/donation_request_form.html', {'form': form})

def donation_success(request):
    return render(request, 'users/donation-success.html')

def request_failure(request,blood_request_id):
    blood_request = get_object_or_404(BloodRequest, id=blood_request_id)
    return render(request, 'users/request_failure.html', {'blood_request': blood_request})


@login_required
def request_success(request, blood_request_id):
    # Fetch the BloodRequest object with the provided ID or return a 404 page if not found
    blood_request = get_object_or_404(BloodRequest, id=blood_request_id)
    cost = blood_request.quantity * 600
    return render(request, 'users/request_success.html', {'blood_request': blood_request,'cost':cost})

@login_required
def request_failure(request):
    blood_bank = request.POST.get('blood_bank')  # Assuming you can retrieve the blood bank from the request
    blood_group = request.POST.get('blood_group')  # Assuming you can retrieve the blood group from the request

    try:
        inventory = BloodInventory.objects.get(
            blood_bank=blood_bank,
            blood_group=blood_group,
        )
        available_quantity = inventory.quantity
    except BloodInventory.DoesNotExist:
        available_quantity = 0  # Set default value if the BloodInventory does not exist

    context = {
        'available_quantity': available_quantity
    }

    return render(request, 'users/request_failure.html', context)
@login_required
def submit_blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_group = form.cleaned_data['blood_group']
            quantity = form.cleaned_data['quantity']
            blood_bank = form.cleaned_data['blood_bank']

            # Check if the requested blood group and quantity are available in the blood bank's inventory
            try:
                inventory = BloodInventory.objects.get(
                    blood_bank=blood_bank,
                    blood_group=blood_group,
                )

                if inventory.quantity >= quantity:
                    # Create a new BloodRequest object with status 'Accepted'
                    blood_request = BloodRequest(
                        user=request.user,
                        blood_bank=blood_bank,
                        blood_group=blood_group,
                        quantity=quantity,
                        status='Accepted'
                    )
                    blood_request.save()

                    # Decrement the blood bank's inventory
                    inventory.quantity -= quantity
                    inventory.save()

                    # Redirect to a success page
                    return redirect('request_success1', blood_request_id=blood_request.id)

            except BloodInventory.DoesNotExist:
                blood_request = BloodRequest(
                    user=request.user,
                    blood_bank=blood_bank,
                    blood_group=blood_group,
                    quantity=quantity,
                    status='Rejected'
                )
                blood_request.save()  # Blood group not found in the inventory

            # If the blood request cannot be fulfilled, set status to 'Rejected'
            blood_request = BloodRequest(
                user=request.user,
                blood_bank=blood_bank,
                blood_group=blood_group,
                quantity=quantity,
                status='Rejected'
            )
            blood_request.save()

            # Redirect to a page indicating the request is rejected
            return redirect('request_failure')

    else:
        form = BloodRequestForm()

    return render(request, 'users/submit_blood_request.html', {'form': form})

@login_required
def user_past_requests(request):
    # Query the BloodRequest model to retrieve the user's past requests
    user_requests = BloodRequest.objects.filter(user=request.user).order_by('-requested_at')

    return render(request, 'users/user_past_requests.html', {'user_requests': user_requests})
