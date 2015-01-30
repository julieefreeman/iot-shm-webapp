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
    data = {'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/dashboard.html', data, context)

@login_required
def real_time(request, building_num):
    context = RequestContext(request)
    data = {'curr_building':Building.objects.get(number=building_num),
            'all_buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/real_time.html', data, context)

@login_required
def long_term(request, building_num):
    context = RequestContext(request)
    data = {'curr_building':Building.objects.get(number=building_num),
            'all_buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/long_term.html', data, context)

@login_required
def building_info(request, building_num):
    context = RequestContext(request)
    data = {'curr_building':Building.objects.get(number=building_num),
            'all_buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/building_info.html', data, context)

@login_required
def my_buildings(request):
    context = RequestContext(request)
    data = {'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/my_buildings.html', data, context)

@login_required
def change_password(request):
    data = {'buildings':Building.objects.filter(manager=request.user)}
    context = RequestContext(request)

    if request.method == 'POST':
        curr_pass = request.POST['curr_pass']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']
        user = authenticate(username=request.user.username, password=curr_pass)

        if user:
            if new_pass==confirm_pass:
                user.password = new_pass
                return HttpResponseRedirect('/iotshm/change_password/complete/')
            else:
                return HttpResponse("Confirmation of password failed.")
        else:
            print("Invalid current password")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('registration/change_password.html', data, context)

@login_required
def change_password_complete(request):
    context = RequestContext(request)
    return render_to_response('registration/change_password_complete.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    context = RequestContext(request)
    return render_to_response('registration/logout.html', {}, context)

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
        return render_to_response('registration/login.html', {}, context)
