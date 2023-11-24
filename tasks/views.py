from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    #print(request.method, request.POST)
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Register User on the admin DB
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()

                #To save the sessionid on the cookies
                login(request, user)

                return redirect('tasks')
            except IntegrityError: 
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        "tasks": tasks
    })

@login_required
def tasks_completed(request):
    tasks = get_list_or_404(Task, datecompleted__isnull=False)
    
    return render(request, 'tasks_completed.html', {
        "tasks": tasks
    })

@login_required
def task_detail(request, id):
    if request.method == 'GET':
        #pk: Primary Key. Id relacionado con Db de usuarios.
        task = get_object_or_404(Task, pk=id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "tasks_detail.html", {
            'form': form,
            "task": task
        })
    else:
        try:
            #pk: Primary Key. Id relacionado con Db de usuarios.
            task = get_object_or_404(Task, pk=id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()

            return redirect('tasks')
        except ValueError:
            return render(request, "tasks_detail.html", {
                'form': form,
                "task": task,
                'error': 'Error updating task'         
            })
        
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(
            request, "create_task.html", {
                'form': TaskForm           
            })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()

            return redirect('tasks')
        except ValueError:
            return render( request, "create_task.html", {
                'form': TaskForm ,
                'error': 'Please provide valid data'         
            })

@login_required
def complete_task(request, id):
    #pk: Primary Key. Id relacionado con Db de usuarios.
    task = get_object_or_404(Task, pk=id, user=request.user)
    
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()

        return redirect('tasks')

@login_required
def delete_task(request, id):
    #pk: Primary Key. Id relacionado con Db de usuarios.
    task = get_object_or_404(Task, pk=id, user=request.user)
    
    if request.method == 'POST':
        task.delete()

        return redirect('tasks')

@login_required
def sign_out(request):
    logout(request)
    return render(request, 'home.html')

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                 'error': 'Username and password is incorrect'
            })
        else:
            #To save the sessionid on the cookies
            login(request, user)
            return redirect('tasks')