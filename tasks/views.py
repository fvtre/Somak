from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    tasks = Task.objects.all()  # Obtener todas las tareas de todos los usuarios
    return render(request, 'home.html', {'tasks': tasks})

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST ['password2']:
            try:    
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(tasks)
            except:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Username already exists'
                })
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Password do not match'
                })
 
@login_required       
def tasks (request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def signout (request):
    logout(request)
    return redirect('home')

def signin (request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm 
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required 
def create_task (request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST, request.FILES)
            new_task = form.save(commit=False)
            new_task.user = request.user 
            new_task.save()
            print(new_task)
            return redirect('home')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valida data'
            })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Mueve esto fuera del bloque if

    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})

    else:  # POST request
        try:
            form = TaskForm(request.POST, request.FILES, instance=task)  # Asegúrate de incluir request.FILES
            if form.is_valid():  # Verifica si el formulario es válido antes de guardarlo
                form.save()
                return redirect('tasks')
            else:
                # En caso de que el formulario no sea válido, se retornan los errores
                return render(request, 'task_detail.html', {'task': task, 'form': form, 
                    'error': "Error al actualizar la tarea. Corrige los errores."})

        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task, 
                'form': form,
                'error': "Error updating task"
            })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
