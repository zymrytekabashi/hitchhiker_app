from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password= password)
        request.session['uid']= user.id
        return redirect('/dashboard')
    
    
    
        
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/')


# dashboard method
def dashboard(request):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context = {
            'logged_user': User.objects.get(id=request.session['uid']),
            'all_trips': Trip.objects.all()
        }
        return render(request, 'dashboard.html', context)


def new_trip(request):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context = {
            'logged_user': User.objects.get(id=request.session['uid']),
        }
        return render(request, 'new_trip.html', context)


def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        new_trip = Trip.objects.create(location = request.POST['location'], desc = request.POST['desc'],
                                       seats = request.POST['seats'], posted_by = User.objects.get(id=request.session['uid']))
        return redirect('/dashboard')
    return redirect('/trips/new')

def edit_trip(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context={
            'edit_trip': Trip.objects.get(id=id),
            'logged_user': User.objects.get(id=request.session['uid']),
        }
        
        return render(request, 'edit.html', context)


# update trip
def update(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            str_id=str(id)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/trips/edit/{str_id}')
        else:
            str_id=str(id)
            edit_trip=Trip.objects.get(id=id)
            edit_trip.location=request.POST['location']
            edit_trip.desc=request.POST['desc']
            edit_trip.seats=request.POST['seats']
            edit_trip.save()
        
        return redirect('/dashboard')
        
    return redirect('/dashboard')

def view_trip(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context = {
            'viewed_trip' : Trip.objects.get(id=id),
            'logged_user': User.objects.get(id=request.session['uid']),
            'all_comments': Comment.objects.all()
        }
        return render(request, 'one_trip.html', context)

    
def reserve_seat(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        trip=Trip.objects.get(id=id)
        trip.seats -=1
        trip.save()
        
        return redirect('/dashboard')
        
def add_comment(request, trip_id):
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        str_id=str(trip_id)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/{str_id}')
    else:
        str_id=str(trip_id)
        new_comment = Comment.objects.create(comment = request.POST['comment'], 
                                             poster = User.objects.get(id=request.session['uid']),
                                             trip = Trip.objects.get(id=trip_id))
        return redirect(f'/trips/{str_id}')
    return redirect('/trips/{str_id}')



#delete 
def destroy(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        Trip.objects.get(id=id).delete()
        return redirect('/dashboard')
    
# log out 
def log_out(request):
    request.session.clear()
    return redirect('/')