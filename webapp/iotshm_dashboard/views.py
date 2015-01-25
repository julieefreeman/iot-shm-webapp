# Create your views here.
from iotshm_dashboard.forms import UserForm
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from iotshm_dashboard.models import Building

def index(request):
    context = {}
    return render(request, 'iotshm_dashboard/index.html', context)

def about(request):
    context = RequestContext(request)
    return render_to_response('iotshm_dashboard/about.html', {}, context)

def contact(request):
    context = RequestContext(request)
    return render_to_response('iotshm_dashboard/contact_us.html', {}, context)

@login_required
def dashboard(request):
    context = RequestContext(request)
    data = {'buildings':Building.objects.all()}
    return render_to_response('iotshm_dashboard/dashboard.html', data, context)

@login_required
def user_logout(request):
    logout(request)
    context = RequestContext(request)
    return render_to_response('iotshm_dashboard/logout.html', {}, context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/iotshm/dashboard/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('iotshm_dashboard/login.html', {}, context)

# currently not implementing the register functionality
# the admin must create users and their buildings through the admin portal
def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()
    return render_to_response(
        'iotshm_dashboard/register.html',
            {'user_form': user_form, 'registered': registered},
            context)