#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Project, Task
from .forms import CreateNewTask, CreateNewProject

# Create your views here.

def index(request):
    title = "Welcome to the jungle!!!"
    return render(request, "index.html", {
        "title": title
    })

def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello world %s</h1>" % username)

def about(request):
    return render(request, "about.html")

def projects(request):
    #projects = list(Project.objects.values())
    #projects = get_list_or_404(Project, id=id)
    projects = Project.objects.all()
    return render(request, "projects/projects.html", {
        "projects": projects,
        "project_detail_path": "project_detail"
    })

def task(request):
    #task = Task.objects.get(id=id)
    #task = get_list_or_404(Task, id=id)
    tasks = Task.objects.all()
    return render(request, "task/task.html", {
        "tasks": tasks
    })

def create_task(request):
    print(request)
    if request.method == 'GET':
        return render(request, "task/create_task.html", {
            "form": CreateNewTask()
        })
    else:
        Task.objects.create(title=request.POST['title'], description=request.POST['description'], project_id=2)
        return redirect('task')
    
def create_project(request):
    if request.method == 'GET':
        return render(request, "projects/create_project.html", {
                "form": CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST['name'])
        return redirect('projects')

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, "projects/detail.html", {
        "project": project,
        "tasks": tasks
    })