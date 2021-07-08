from django.shortcuts import render,redirect
# Create your views here.
from django.contrib import messages
from .models import *
import bcrypt

# render home page
def home(request):
    return render(request, "index.html")

#process registration and redirect
def register(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key,error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(email=request.POST['email'].lower(), password=pw_hash, first_name=request.POST['first_name'], last_name=request.POST['last_name'],birthday=request.POST['birthday'])
        request.session['user_id'] = user.id #generated by django
        request.session['first_name'] = user.first_name
        messages.success(request, "Registered successfully :)")
        return redirect("/success")    

# process login info and redirect
def login(request):
    errors = User.objects.login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'].lower())
        if len(user) < 1:
            messages.error(request, "No User for that email")
            return redirect("/")
        
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print(f"LOG - Setting session value 'user_id' = {user[0].id}")
            request.session['user_id'] = user[0].id
            request.session['first_name'] = user[0].first_name
            return redirect("/success")
        else:
            messages.error(request, "Incorrect Password!")
            return redirect("/")

# logout and redirect
def logout(request):
    request.session.clear()
    messages.success(request, "Log out successful!")
    print(f"LOG - Log out successful, redirecting to home")  
    return redirect("/")

# render success page
def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "Permission Denied")
        return redirect("/")
    context = {
        "user_id" : request.session['user_id'],
        "first_name": request.session['first_name']       
    }
    print(f"LOG - Rendering success page")
    return render(request, "success.html", context)