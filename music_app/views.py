from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MusicFile
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def home(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        music_files = MusicFile.objects.filter(upload_type=MusicFile.PUBLIC)
    else:
        music_files = MusicFile.objects.filter(
            Q(user=user) | Q(upload_type=MusicFile.PUBLIC)).distinct()
    return render(request, 'music_app/home.html', {'music_files': music_files})


@login_required
def upload_music(request):
    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES['file']
        upload_type = request.POST.get('upload_type')
        allowed_emails = request.POST.getlist('allowed_emails')

        if upload_type not in [MusicFile.PUBLIC, MusicFile.PRIVATE, MusicFile.PROTECTED]:
            return HttpResponseBadRequest("Invalid access level.")

        music_file = MusicFile(
            user=request.user, title=title, file=file, upload_type=upload_type)

        if upload_type == MusicFile.PROTECTED:
            allowed_users = User.objects.filter(email__in=allowed_emails)
            music_file.allowed_emails = ','.join(allowed_emails)

        music_file.save()
        return redirect('home')

    return render(request, 'music_app/upload.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return HttpResponseBadRequest("User with this email already exists.")
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.is_active = False
            user.save()
            return redirect('registration_success')
    return render(request, 'music_app/register.html')


def registration_success(request):
    return render(request, 'music_app/registration_success.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'music_app/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'logged out Successfully')
    return redirect('home')
