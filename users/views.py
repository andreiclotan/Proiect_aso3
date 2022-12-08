from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Room,Message
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model


# Create your views here.
def login_user(request):
  if request.user.is_authenticated:
        User = get_user_model()
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'authenticate/home.html',{'users':users})
  if request.method == "POST" :
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        User = get_user_model()
        users = User.objects.all()
        print(users)
        return render(request, 'authenticate/home.html',{'users':users})
    else:
        messages.success(request,"Invalid credentials")
        return redirect('login')
  else:
    return render(request, 'authenticate/login.html',{})
    

def logout_user(request):
  logout(request)
  messages.success(request,"Logged out.")
  return redirect('login')

def room(request, room):
  username = request.GET.get('username')
  room_details = Room.objects.get(name=room)
  return render(request, 'authenticate/room.html',{
    'username': username,
    'room': room,
    'room_details': room_details
  })

def checkview(request):
  room = request.POST['room_name']
  if room < request.user.username:
    name = room
  else:
    name = request.user.username
  if Room.objects.filter(name=name).exists():
    return redirect('/'+name+'/?username='+request.user.username)
  else:
    new_room = Room.objects.create(name=name)
    new_room.save()
    return redirect('/'+name+'/?username='+request.user.username)

def send(request):
  message = request.POST['message']
  username = request.POST['username']
  room_id = request.POST['room_id']
  new_message = Message.objects.create(message = message, user=username, room=room_id)
  new_message.save()
  return HttpResponse('Message send')

def getMessages(request, room):
  room_details = Room.objects.get(name = room)
  messages = Message.objects.filter(room=room_details.id)
  return JsonResponse({'messages': list(messages.values())})