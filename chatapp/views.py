from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, "chathome.html")


def room(request):
    if request.method=="POST":
        room_name=request.POST['roomname']
        person_name=request.POST['username']
        return render(
            request, "chatroom.html", {"room_name": room_name, "person_name": person_name}
        )
