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
    tasks = Task.objects.all().order_by('-created_at')  # Ordenar de más recientes a más antiguas
    return render(request, 'home.html', {'tasks': tasks})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # Verificar si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear el usuario con los nuevos campos
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],  # Nuevo campo email
                    first_name=request.POST['first_name'],  # Nuevo campo first_name
                    last_name=request.POST['last_name']  # Nuevo campo last_name
                )
                user.save()  # Guardar el usuario
                login(request, user)  # Iniciar sesión automáticamente
                return redirect('tasks')  # Redirigir a la vista de tareas
            except Exception as e:
                # Capturar cualquier error y mostrar un mensaje
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": f'Error al crear el usuario: {str(e)}'
                })
        else:
            # Si las contraseñas no coinciden
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Las contraseñas no coinciden.'
            })

 
@login_required       
def tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
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
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST, request.FILES)
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.user = request.user  # Asociar la tarea al usuario actual
                new_task.save()
                print(new_task)  # Ver el objeto creado en la consola (esto es opcional)
                return redirect('home')  # Redirigir a la página de inicio
            else:
                # Aquí se imprime cada uno de los errores
                print(form.errors)  # Esto imprimirá los errores del formulario en la consola
                return render(request, 'create_task.html', {
                    'form': form,  # Pasar el formulario con los errores
                    'error': 'Por favor, provee datos válidos.'
                })
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'Hubo un error al crear la tarea.'
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

def casadepaz(request):
    tasks = Task.objects.filter(category='casadepaz').order_by('-created_at')
    return render(request, 'casadepaz.html', {'tasks': tasks})

def aviva2(request):
    tasks = Task.objects.filter(category='aviva2').order_by('-created_at')
    return render(request, 'aviva2.html', {'tasks': tasks})

def avivakids(request):
    tasks = Task.objects.filter(category='avivakids').order_by('-created_at')
    return render(request, 'avivakids.html', {'tasks': tasks})

def jovenes(request):
    tasks = Task.objects.filter(category='jovenes').order_by('-created_at')
    return render(request, 'jovenes.html', {'tasks': tasks})
