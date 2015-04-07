# Create your views here.
from iotshm_dashboard.forms import UserForm
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from iotshm_dashboard.models import Building, HealthRDS, MagnitudeRDS, SensorRDS
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
import json
import datetime
# from datetime import datetime, timedelta
from random import randint
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware, utc

def index(request):
    context = {}
    return render(request, 'iotshm_dashboard/index.html', context)

def about(request):
    context = RequestContext(request)
    return render_to_response('iotshm_dashboard/about.html', {}, context)

def contact(request):
    context = RequestContext(request)

    if request.method == 'POST':
        subject = request.POST['name']+': '+request.POST['email']
        message = request.POST['message']
        if subject and message:
            try:
                send_mail(subject, message, 'iot.shm@gmail.com', ['iot.shm.helpdesk@gmail.com'])
            except BadHeaderError:
                messages.error(request,'Invalid header found.')
                return render_to_response('iotshm_dashboard/contact_us.html', {}, context)
            message = 'We have received your concern! We will be getting back to you shortly.'
            send_mail("IoT SHM - your question received", message, 'iot.shm@gmail.com', [request.user.email])
            return HttpResponseRedirect('/iotshm/contact/thanks/')
        else:
            messages.error(request,'Make sure all fields are entered and valid.')
            return render_to_response('iotshm_dashboard/contact_us.html', {}, context)
    else:
        return render_to_response('iotshm_dashboard/contact_us.html', {}, context)

def contact_thanks(request):
    context = RequestContext(request)
    return render_to_response('iotshm_dashboard/contact_thanks.html', {}, context)

@login_required
def dashboard(request):
    context = RequestContext(request)
    if request.user.username == 'admin':
        data = {'buildings':Building.objects.all()}
    else:
        data = {'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/dashboard.html', data, context)

@login_required
def real_time(request, building_num):
    context = RequestContext(request)
    curr_building = Building.objects.get(number=building_num)
    if request.user.username == 'admin':
        data = {'sensors':SensorRDS.objects.using('data').filter(building_id=building_num),
                'curr_building':curr_building,
                'buildings':Building.objects.all()}
    else:
        data = {'sensors':SensorRDS.objects.using('data').filter(building_id=building_num),
                'curr_building':curr_building,
                'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/real_time.html', data, context)


@login_required
def long_term(request, building_num):
    context = RequestContext(request)
    if request.user.username == 'admin':
        data = {'curr_building':Building.objects.get(number=building_num),
                'buildings':Building.objects.all()}
    else:
        data = {'curr_building':Building.objects.get(number=building_num),
                'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/long_term.html', data, context)

@login_required
def building_info(request, building_num):
    context = RequestContext(request)
    if request.user.username == 'admin':
        data = {'curr_building':Building.objects.get(number=building_num),
                'buildings':Building.objects.all()}
    else:
        data = {'curr_building':Building.objects.get(number=building_num),
                'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/building_info.html', data, context)

@login_required
def my_buildings(request):
    context = RequestContext(request)
    if request.user.username == 'admin':
        data = {'buildings':Building.objects.all()}
    else:
        data = {'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('iotshm_dashboard/my_buildings.html', data, context)

@login_required
def change_password(request):
    if request.user.username == 'admin':
        data = {'buildings':Building.objects.all()}
    else:
        data = {'buildings':Building.objects.filter(manager=request.user)}
    context = RequestContext(request)

    if request.method == 'POST':
        curr_pass = request.POST['curr_pass']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']
        user = authenticate(username=request.user.username, password=curr_pass)

        if user:
            if new_pass==confirm_pass:
                send_mail('Password successfully changed!', 'Password changed for your IoT-SHM account!', 'iot.shm@gmail.com',[user.email], fail_silently=False)
                user.set_password(new_pass)
                user.save()
                login(request, user)
                return HttpResponseRedirect('/iotshm/change_password/complete/')
            else:
                messages.error(request,'New password not confirmed - try again.')
                return HttpResponseRedirect('/iotshm/change_password/')
        else:
            messages.error(request,'Invalid current password - try again.')
            return HttpResponseRedirect('/iotshm/change_password/')
    else:
        return render_to_response('registration/change_password.html', data, context)

@login_required
def change_password_complete(request):
    context = RequestContext(request)
    if request.user.username == 'admin':
        data = {'buildings':Building.objects.all()}
    else:
        data = {'buildings':Building.objects.filter(manager=request.user)}
    return render_to_response('registration/change_password_complete.html', data, context)

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
                messages.error(request,'Your account is disabled.')
        else:
            messages.error(request,'Invalid current password - try again.')
            return render_to_response('registration/login.html', {}, context)
    else:
        return render_to_response('registration/login.html', {}, context)


def real_time_ajax_x(request,building_num):
    curr_building_sensors = SensorRDS.objects.using('data').filter(building_id=building_num)
    curr_building_sensors = [str(s.id) for s in curr_building_sensors]
    timestamps = HealthRDS.objects.using('data').filter(timestamp__lt=timezone.now()).order_by('timestamp').reverse()
    json_response = {}
    if (timestamps.count() > 0):
        ts = timestamps[0].timestamp
        Magnitudes = MagnitudeRDS.objects.using('data').filter(reading_type=0).filter(timestamp=make_aware(ts,utc))
        for m in Magnitudes:
            if m.sensor_id in curr_building_sensors:
                if not m.sensor_id in json_response:
                    json_response[m.sensor_id] = {"x_data": []}
                # json_response[m.sensor_id]["x_data"].append({"frequency": m.frequency,"magnitude": m.value})
                json_response[m.sensor_id]["x_data"].append([m.frequency,m.value])
        r = {"data":json_response, "time":ts}
    return HttpResponse(json.dumps(r), content_type='application/json')

def real_time_ajax_y(request,building_num):
    curr_building_sensors = SensorRDS.objects.using('data').filter(building_id=building_num)
    curr_building_sensors = [str(s.id) for s in curr_building_sensors]
    timestamps = HealthRDS.objects.using('data').filter(timestamp__lt=timezone.now()).order_by('timestamp').reverse()
    json_response = {}
    if (timestamps.count() > 0):
        ts = timestamps[0].timestamp
        Magnitudes = MagnitudeRDS.objects.using('data').filter(reading_type=1).filter(timestamp=make_aware(ts,utc))
        for m in Magnitudes:
            if m.sensor_id in curr_building_sensors:
                if not m.sensor_id in json_response:
                    json_response[m.sensor_id] = {"y_data": []}
                # json_response[m.sensor_id]["y_data"].append({"frequency": m.frequency,"magnitude": m.value})
                json_response[m.sensor_id]["y_data"].append([m.frequency,m.value])
        r = {"data":json_response, "time":ts}

    return HttpResponse(json.dumps(json_response), content_type='application/json')

def real_time_ajax_z(request,building_num):
    curr_building_sensors = SensorRDS.objects.using('data').filter(building_id=building_num)
    curr_building_sensors = [str(s.id) for s in curr_building_sensors]
    timestamps = HealthRDS.objects.using('data').filter(timestamp__lt=timezone.now()).order_by('timestamp').reverse()
    json_response = {}
    if (timestamps.count() > 0):
        ts = timestamps[0].timestamp
        Magnitudes = MagnitudeRDS.objects.using('data').filter(reading_type=1).filter(timestamp=make_aware(ts,utc))
        for m in Magnitudes:
            if m.sensor_id in curr_building_sensors:
                if not m.sensor_id in json_response:
                    json_response[m.sensor_id] = {"z_data": []}
                # json_response[m.sensor_id]["z_data"].append({"frequency": m.frequency,"magnitude": m.value})
                json_response[m.sensor_id]["z_data"].append([m.frequency,m.value])
        r = {"data":json_response, "time":ts}

    return HttpResponse(json.dumps(json_response), content_type='application/json')

def health(request,building_num):
    curr_building_sensors = SensorRDS.objects.using('data').filter(building_id=building_num)
    curr_building_sensors = [str(s.id) for s in curr_building_sensors]
    unhealthys = HealthRDS.objects.using('data')\
        .filter(timestamp__gt=(make_aware((datetime.datetime.now() - datetime.timedelta(minutes=5)),utc)))\
        .filter(sensor_id__in = curr_building_sensors)\
        .filter(healthy=0)

    json_response = {'healthy':len(unhealthys)==0}
    return HttpResponse(json.dumps(json_response), content_type='application/json')

@login_required
def sensors(request,building_num):
    context = RequestContext(request)
    data = {'curr_building': Building.objects.get(number=building_num),
            'buildings': Building.objects.filter(manager=request.user),
            'sensors': SensorRDS.objects.using('data').filter(building_id=building_num)}

    if request.method == 'POST':
        return render_to_response('iotshm_dashboard/sensors.html', {}, context)
    else:
        return render_to_response('iotshm_dashboard/sensors.html', data, context)