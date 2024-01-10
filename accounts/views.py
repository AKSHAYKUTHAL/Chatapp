from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth,messages
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "accounts/register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('chat/')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')
