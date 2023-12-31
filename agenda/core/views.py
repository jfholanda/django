import json

from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import Http404, JsonResponse
from datetime import datetime, timedelta

# Create your views here.

# def index(request):
#     return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=2) #permitindo ver até 2 horas atrasado
    if usuario.username == 'admin':
        eventos = Evento.objects.all()
        response = {'eventos': eventos, 'usuario': usuario}
    else:
        eventos = Evento.objects.filter(usuario=usuario, 
                                        data_evento__gt=data_atual)
        
        response = {'eventos': eventos, 'usuario': usuario}

    return render(request, 'agenda.html', response)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        try:
            dados['evento'] = Evento.objects.get(id=id_evento)
        except Exception:
            raise Http404()
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()

        else:
            Evento.objects.create(titulo=titulo, 
                                  data_evento=data_evento, 
                                  descricao=descricao, 
                                  usuario=usuario)
                
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    if usuario.username == 'admin':
        eventos = Evento.objects.all().values('id', 'titulo', 'usuario')
    else:
        eventos = Evento.objects.filter(usuario=usuario).values('id', 'titulo')

    return JsonResponse(list(eventos), safe=False)

@login_required(login_url='/login/')
def historico_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=2)
    eventos = Evento.objects.filter(usuario=usuario, data_evento__lt=data_atual)
    response = {'eventos': eventos, 'usuario': usuario}
    
    return render(request, 'historico.html', response)


