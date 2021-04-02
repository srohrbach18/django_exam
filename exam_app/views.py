from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        ) 
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['greeting'] = user.first_name
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'all_groups': Group.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'main_page.html', context)

def create_group(request):
    errors = Group.objects.group_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/success')
    else:
        user = User.objects.get(id=request.session["user_id"])
        group = Group.objects.create(
            org_name = request.POST['org_name'],
            desc = request.POST['desc'],
            creator = user
        )
        user.joined_groups.add(group)
        return redirect(f'/success')
    
def show_one(request, group_id):
    context = {
        'group': Group.objects.get(id=group_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show_one.html", context)

def join(request, group_id):
    user = User.objects.get(id=request.session["user_id"])
    group = Group.objects.get(id=group_id)
    user.joined_groups.add(group)
    return redirect(f'/groups/{group.id}')

def leave(request, group_id):
    user = User.objects.get(id=request.session["user_id"])
    group = Group.objects.get(id=group_id)
    user.joined_groups.remove(group)
    return redirect('/success')

def delete_group(request, group_id):
    delete = Group.objects.get(id=group_id)
    delete.delete()
    return redirect('/success')