from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            group_name = request.POST.get('register_user_group')
            user = authenticate(username=username, password=password)
            group = Group.objects.get(name=group_name)

            if group:
                group.user_set.add(user)
            login(request, user)

            return redirect('index')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', context={'form': form})
