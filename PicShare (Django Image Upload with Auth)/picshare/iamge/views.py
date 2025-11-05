from ntpath import exists
from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Image
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

# Create your views here.
@login_required
def upload_image(request):
    images = Image.objects.all()  # Changed to lowercase, moved outside if/else
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():  # Fixed: was is_vaild() - typo
            form.save()
            return redirect('image_list')
    else:
        form = ImageForm()

    return render(request, 'iamge/upload.html', {'form': form, 'images': images})  # Fixed: Images to images


def image_list(request):
    images = Image.objects.all()  # Changed Images to images (lowercase)
    return render(request, 'iamge/image_list.html', {'images': images})  # Fixed: Images to images


def login_view(request):
    if request.method=="POST":
        username =request.POST.get('username')
        password = request.POST.get('password')

    # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username does not exist')
            return redirect('login')
        
        user=authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

        auth_login(request, user)
        next_url = request.GET.get('next') or request.POST.get('next')
        return redirect(next_url or 'image_list')
    
    return render(request, 'iamge/login.html')

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

    # Check if a user with the provided username already exists
        user=User.objects.filter(username=username)

        if user is exists:
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        user=User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')
        
        
    return render(request, 'iamge/register.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')
