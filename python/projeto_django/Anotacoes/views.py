from django.shortcuts import render
from .models import Task, Notation
from .forms import Task_Form, Notation_form
from django.http import HttpResponseRedirect, Http404 #type: ignore 
from django.urls import reverse #type: ignore 
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    return render(request, 'Anotacoes/index.html')


@login_required
def tasks(request):
    context = dict()
    tasks = Task.objects.filter(owner = request.user, completed = False).order_by('date')
    context['tasks'] = tasks
    return render(request, 'Anotacoes/tasks.html', context)

@login_required
def task(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404

    notations = task.notation_set.order_by('-date_added')
    context['task'] = task
    context['notations'] = notations
    return render(request, 'Anotacoes/task.html', context)


@login_required
def new_task(request):
    context = dict()
    if request.method != 'POST': #formulário em branco
        form = Task_Form()
    else:
        form = Task_Form(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return HttpResponseRedirect(reverse('tasks'))
    context['form'] = form
    return render(request, 'Anotacoes/new_task.html', context)


@login_required
def new_notation(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = Notation_form()
    else:
        form = Notation_form(data = request.POST)
        if form.is_valid():
            new_notation = form.save(commit=False)
            new_notation.task = task
            new_notation.save()
            return HttpResponseRedirect(reverse('task', args=[task_id]))
    context['task'] = task
    context['form'] = form
    return render(request, 'Anotacoes/new_notation.html', context)


@login_required
def edit_notation(request, notation_id):
    context = dict()
    try:
        notation = Notation.objects.get(id = notation_id)
        task = notation.task
    except Notation.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = Notation_form(instance=notation)
    else:
        form = Notation_form(instance=notation, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task', args=[task.id]))
        
    context['notation'] = notation
    context['task'] = task
    context['form'] = form
    return render(request, 'Anotacoes/edit_notation.html', context)


@login_required
def delete_task(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect(reverse('tasks'))
    context['task'] = task
    return render(request, 'Anotacoes/delete_task.html', context)


@login_required
def delete_notation(request, notation_id):
    context = dict()
    try:
        notation = Notation.objects.get(id = notation_id)
        task = notation.task
    except Notation.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method == 'POST':
        notation.delete()
        return HttpResponseRedirect(reverse('task', args=[task.id]))
    context['notation'] = notation
    context['task'] = task
    return render(request, 'Anotacoes/delete_notation.html', context)


@login_required
def my_day(request):
    context = dict()
    data_atual = datetime.now().date()
    tasks = Task.objects.filter(owner=request.user, date=data_atual, completed = False).order_by('date')
    context['tasks'] = tasks
    return render(request, 'Anotacoes/my_day.html', context)


@login_required
def tasks_important(request):
    context = dict()
    tasks = Task.objects.filter(owner = request.user, important= True).order_by('date')
    context['tasks'] = tasks
    return render(request, 'Anotacoes/tasks_important.html', context)


@login_required
def mark_important(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method == 'POST':
        task.important = True
        task.save()
        return HttpResponseRedirect(reverse('tasks'))
    context['task'] = task
    return render(request, 'Anotacoes/mark_important.html', context)


@login_required
def mark_completed(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method == 'POST':
        task.completed = True
        task.save()
        return HttpResponseRedirect(reverse('tasks'))
    context['task'] = task
    return render(request, 'Anotacoes/mark_completed.html', context)


@login_required
def tasks_completed(request):
    context = dict()
    tasks = Task.objects.filter(owner = request.user, completed = True).order_by('date')
    context['tasks'] = tasks
    return render(request, 'Anotacoes/tasks_completed.html', context)


@login_required
def restore_task(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        task.completed = False 
        task.save()
        return HttpResponseRedirect(reverse('tasks'))
    context['task'] = task
    return render(request, 'Anotacoes/restore_task.html', context)


@login_required
def remove_important(request, task_id):
    context = dict()
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if task.owner != request.user:
        raise Http404
    if request.method == 'POST':
        task.important = False
        task.save()
        return HttpResponseRedirect(reverse('tasks'))
    context['task'] = task
    return render(request, 'Anotacoes/remove_important.html', context)
