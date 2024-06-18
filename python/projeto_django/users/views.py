from django.http import HttpResponseRedirect #type: ignore
from django.urls import reverse #type: ignore
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from .models import Users
from .forms import User_Form

def register(request):
    context = dict()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method != 'POST': # ainda não foi preenchido
        form = User_Form()
    else:
        #processa o formulário preenchido
        form = User_Form(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password = request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    context['form'] = form
    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

