from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def index(request):
    return render(request, 'index.html')


def register(request):
    form = RegisterForm()
    mydict = {'form': form}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            mydict['form'] = form
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})
    return render(request, 'register.html', context=mydict)
    # if request.method == 'POST':
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return render(request, 'login.html', {'success': "Registration successful. Please login."})
    #     else:
    #         error_message = form.errors.as_text()
    #         return render(request, 'register.html', {'error': error_message})
    #
    # return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})


@login_required
def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})


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

def handling_404(request, exception):
    return render(request, '404.html', {})


def handling_500(request):
    return render(request, '500.html')
