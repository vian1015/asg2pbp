from django.shortcuts import render
from todolist.models import Task
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/todolist/login/')
def show_todolist(request):
    task_list = Task.objects.filter(user=request.user)
    context = {
        'task_list': task_list,
        'name': 'Jovian',
        'npm': 2106720891,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "todolist.html", context)

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, 
                            description=description, 
                            user=request.user, 
                            date=datetime.datetime.now())
        response = HttpResponseRedirect(reverse('todolist:show_todolist'))
        response.set_cookie('last_update', str(datetime.datetime.now()))
        return response

    context = {}
    return render(request, 'create_task.html', context)

def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    response = HttpResponseRedirect(reverse('todolist:show_todolist'))
    response.set_cookie('last_update', str(datetime.datetime.now()))
    return response

def inverse_checkbox(request, task_id):
    task = Task.objects.get(id=task_id)
    print(task.is_finished)
    task.is_finished = not task.is_finished
    task.save()
    response = HttpResponseRedirect(reverse('todolist:show_todolist'))
    response.set_cookie('last_update', str(datetime.datetime.now()))
    return response

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created!')
            return redirect('todolist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # login first
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # create response
            response.set_cookie('last_login', str(datetime.datetime.now())) # create last_login cookie and add it to response
            return response
        else:
            messages.info(request, 'Wrong Username or Password!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return response
