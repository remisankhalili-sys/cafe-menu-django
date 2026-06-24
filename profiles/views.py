from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .form import ProfileForm

@login_required
def panel_user(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/panel.html', {'profile': profile})
    
@login_required   
def profile_page(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profiles/profile_page.html', {'profile': profile})

@login_required  
def edit_profile(request):
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            
            form.save()
            return redirect('profile_page')
    else:
        
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form,'profile': profile})
        