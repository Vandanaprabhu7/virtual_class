from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import PresentMeeting
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

@login_required

def dashboard(request):
    is_staff = request.user.is_staff
    return render(request, 'dashboard.html', {'name': request.user.first_name, 'is_staff': is_staff,'id':request.user.id})

@login_required
def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name+" ["+request.user.email.split('@')[0]+"]",'id':request.user.id})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')


@login_required
def join_room(request):
        is_staff = request.user.is_staff
    
        if request.method == 'POST':
            room_id = request.POST.get('roomID')
        
            if request.user.is_staff:
                if not PresentMeeting.objects.filter(room_id=room_id).exists():
                    present_meeting = PresentMeeting.objects.create(room_id=room_id, user=request.user)
                    present_meeting.add_participant(request.user.id)
                    present_meeting.save()
                    messages.success(request, "Meeting created successfully.")
                    return render(request, 'videocall.html', {'name': request.user.first_name + " [" + request.user.email.split('@')[0] + "]", 'room_id': room_id, 'is_staff': is_staff,'id':request.user.id})
                else:
                    present_meeting = PresentMeeting.objects.get(room_id=room_id)
                    participants = present_meeting.get_participants()
                    if request.user.id in participants:
                        messages.error(request, "You've already joined this meeting.")
                    else:
                        present_meeting.onprogress = True
                        present_meeting.add_participant(request.user.id)
                        present_meeting.save()
                        return render(request, 'videocall.html', {'name': request.user.first_name + " [" + request.user.email.split('@')[0] + "]", 'room_id': room_id, 'is_staff': is_staff,'id':request.user.id})
            else:
                if not PresentMeeting.objects.filter(room_id=room_id).exists():
                    messages.error(request, "Invalid meeting id, please recheck and enter again.")
                else:
                    present_meeting = PresentMeeting.objects.get(room_id=room_id)
                    participants = present_meeting.get_participants()
                    if request.user.id in participants:
                        messages.error(request, "You've already joined this meeting.")
                    else:
                        present_meeting.onprogress = True
                        present_meeting.add_participant(request.user.id)
                        present_meeting.save()
                        return render(request, 'videocall.html', {'name': request.user.first_name + " [" + request.user.email.split('@')[0] + "]", 'room_id': room_id, 'is_staff': is_staff,'id':request.user.id})
        return render(request, 'joinroom.html', {'is_staff': is_staff})