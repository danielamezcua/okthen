from django.shortcuts import render

from django.shortcuts import render, redirect,reverse
from . import forms
from okthen.sessions import validate

def index(request):
        valid = validate(request)
        if valid == True:
            return render(request, 'index.html')
        return valid

def login(request):
    form = forms.Login(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            persona = form.cleaned_data['personas']
            request.session['user'] = persona.nombre
            return redirect(reverse('index'))
    return render(request, 'login.html', {'form':form})

def logout(request):
    valid = validate(request)
    if valid == True:
        request.session.pop('user')
        return redirect(reverse('login'))
    return valid
