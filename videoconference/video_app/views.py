import base64
from io import BytesIO
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import PresentMeeting
from django.contrib import messages
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import sectionDetails
import os

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
                    secdet=sectionDetails.objects.get(user_id=request.user.id)
                    studetns=secdet.getusn(request.user.id)
                    print(studetns)
                    present_meeting = PresentMeeting.objects.create(room_id=room_id, user=request.user)
                    present_meeting.onprogress = True
                    present_meeting.add_participant(request.user.id)
                    present_meeting.save()
                    messages.success(request, "Meeting created successfully.")#here
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


def leave_room(request):
    if request.method == 'GET':
         user_id = request.GET.get('userID')
         room_id = request.GET.get('roomID')
         try:
            present_meeting = PresentMeeting.objects.get(room_id=room_id)
        
            participants = [int(participant_id) for participant_id in present_meeting.participants.strip('[]').split(',') if participant_id]
            
            if int(user_id) in participants:
                participants.remove(int(user_id))

            present_meeting.participants = ','.join(map(str, participants)) if participants else ''
            if len(participants)==0:
                present_meeting.onprogress = False
            present_meeting.add_leave_time(user_id)
            present_meeting.save()

            return redirect('index')
         except PresentMeeting.DoesNotExist:
            return JsonResponse({'error': 'PresentMeeting with room ID {} does not exist'.format(room_id)})
    else:
         return JsonResponse({'message': 'Invalid request method'}, status=400)
    
@login_required
def view_report(request):
    if request.method == 'GET':
        return render(request, 'viewreport.html')
    else:
        roomID = request.POST['roomID']
        try:
            present_meeting = PresentMeeting.objects.get(room_id=roomID)
            intervals = present_meeting.interval
            tot_time = intervals[str(present_meeting.user_id)]
            hours, minutes, seconds = map(int, tot_time.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            entries = []
            for key, time_str in intervals.items():
                user_id = int(key)
                if user_id != present_meeting.user_id:
                    user = User.objects.get(id=user_id)
                    hours, minutes, seconds = map(int, time_str.split(':'))
                    total_seconds2 = hours * 3600 + minutes * 60 + seconds
                    percentage = round((total_seconds2 / total_seconds) * 100,2)
                    entry = {
                        'user_info': f"{user.first_name.strip()} {user.last_name.strip()} [{user.username[:-10]}]",
                        'interval': time_str,
                        'percentage': percentage
                    }
                    entries.append(entry)
            return render(request, 'report.html', {'entries': entries, 'tot_time': tot_time})
        except PresentMeeting.DoesNotExist:
            messages.error(request, "Invalid meeting id, please recheck and enter again.")
        return render(request, 'viewreport.html')

def create_sec(request):
    is_staff = request.user.is_staff
    if request.method == "POST":
        secname = request.POST.get('secname')
        secstudents = request.POST.get('secstudents')
        
        # Create an instance of sectionDetails model
        section = sectionDetails(user=request.user, secname=secname, students=secstudents)
        
        # Save the instance to the database
        section.save()
        
        return render(request, 'createsec.html', {'is_staff': is_staff, 'secname': secname, 'secstudents': secstudents})
    else:
        # Render the form template for GET requests
        return render(request, 'createsec.html', {'is_staff': is_staff})

