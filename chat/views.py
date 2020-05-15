from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    return render(request, 'chat.html', context={
                                        'room_name': room_name,
                                        'username': request.user.username,
                                        })