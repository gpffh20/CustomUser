from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render, redirect
from .forms import CustomUserSigninForm, CustomUserSignupForm


def signup(request):
    form = CustomUserSignupForm()
    # 착한 사용자
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save() #form data를 db에 저장
            login(request, user)
            return redirect("home")
    
    #나쁜 사용자
    return render(request, "newSignup.html", {"form" : form})


def signin(request):
    form = CustomUserSigninForm()
    # 착한 사용자
    if request.method == "POST":
        form = CustomUserSigninForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    
    # bad user
    return render(request, "newSignin.html", {"form" : form})


def signout(request):
    logout(request)
    return redirect("home")

def profile(request):
    create_profile = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {"profile":profile})

def create_profile(request):
    create_profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname')
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect('users:profile')

    return render(request, 'profile.html', {'profile': profile})

        

# # 회원가입
# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(
#                 username=request.POST['username'],
#                 password=request.POST['password1'],
#                 email=request.POST['email'],)
#             profile = Profile(user=user, nickname=request.POST['nickname'], image=request.FILES.get('profile_image'))
#             profile.save()

#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'signup.html')
#     return render(request, 'signup.html')

# # 로그인
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')

# # 로그아웃
# def logout(request):
#   auth.logout(request)
#   return redirect('home')