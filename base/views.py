from multiprocessing import context
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Story, User
from .forms import CustomUserCreationForm, storyForm
from django.db.models import Q


def home(request):
    if request.user.is_authenticated:
        return redirect('stories')

    stories = Story.objects.all()
    context = {
        'stories' : stories
    }
    return render(request, 'home.html', context)


def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid information provided')
    
    context = {
        'form': form,
        'type': 'Signup'
    }

    return render(request, 'authentication.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('stories')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('stories')
            else:
                messages.error(request, 'Password did not match')
        except:
            messages.error(request, 'Username does not exist')

    context = {
        'page': page,
        'type': 'Login'
    }

    return render(request, 'authentication.html', context)

def stories(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    stories = Story.objects.filter(
        Q(title__icontains=q) |
        Q(user__username__icontains=q) |
        Q(user__first_name__icontains=q) |
        Q(user__last_name__icontains=q)
        )[:25]
    context = {
        'stories' : stories
    }
    return render(request, 'stories.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def user(request, username):
    user = User.objects.get(username=username)
    story = Story.objects.filter(user=user)
    context = {
        'user': user,
        'story': story
        }
    return render(request, 'userpage.html', context)


def story(request,username, id):
    story = Story.objects.get(id=id)
    context = {
        'story' : story
    }
    return render(request, 'story.html', context)

def storyWriter(request):
    if not request.user.is_authenticated:
        return redirect('register')

    editor = storyForm()

    if request.method == 'POST':
        editor = storyForm(request.POST)
        if editor.is_valid():
            story = editor.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('stories')

    context = {
        'editor':editor
    }
    return render(request, 'editor.html', context)

def storyEditor(request,username, pk):
    story = Story.objects.get(id=pk)
    editor = storyForm(instance=story)

    if request.user != story.user:
        return redirect('stories')

    if request.method == 'POST':
        editor = storyForm(request.POST, instance=story)
        if editor.is_valid():
            editor.save()
            return redirect('stories')

    context = {
        'editor' : editor
    }
    return render(request, 'editor.html', context)

def storyDeleter(request,username, pk):
    story = Story.objects.get(id=pk)

    if request.user != story.user:
        return redirect('stories')

    if request.method == 'POST':
        story.delete()
        return redirect('home')

    return render(request, 'delete.html', {'story':story})