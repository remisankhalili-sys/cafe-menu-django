from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def profile_page(request):
    context = {}
    return render(request, 'profiles/profile_page.html', context)