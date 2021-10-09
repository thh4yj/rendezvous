# **********************************************************************
#  REFERENCES

#  Title: Building a Simple Search in Django
#  Author: Kevin O'Brien
#  Date: August 30, 2016
#  URL: https://www.kobrien.me/blog/post/building-simple-search-django/
##
# **********************************************************************
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.utils import timezone
from .search import make_search
from .models import Event


from django.views import generic

from .models import Event, EventForm

# Create your views for the events app here.

# Source: https://docs.djangoproject.com/en/3.1/intro/tutorial03/
# Taken from the initial Django tutorial
def event_list_view(request):
    event_list = Event.objects.order_by('-pub_date')
    #event_json = list(event_list)
    #context = {'event_list': event_list, 'event_json': event_json}
    context = {'event_list': event_list}
    return render(request, "events/event.html", context)

# Source: https://docs.djangoproject.com/en/3.1/intro/tutorial03/
# Taken from the initial Django tutorial
def event_detail_view(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event_json = []
        event_json.append({"title": event.title, "address": event.address})
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    return render(request, "events/detail.html", {'event': event, 'event_json': event_json})

# Source: https://docs.djangoproject.com/en/3.1/intro/tutorial04/
# Taken from the initial Django tutorial
def event_view(request):
    form = EventForm()
    return render(request, "events/create-event2.html", {'form': form})
'''
def create_event(request):
    event_title = request.POST.get("eventName")
    event_desc = request.POST.get("eventDesc")
    event_location = request.POST.get("eventLocation")
    start_time = request.POST.get("eventStart")
    end_time = request.POST.get("eventEnd")
    icon = request.FILES.get("eventIcon")
    event = Event(author = request.user, pub_date = timezone.now())
    error = event.exists_required_input(event_title, event_desc, event_location, start_time, end_time)

    if (error == 0):
        event.title = event_title
        event.desc = event_desc
        event.location_name = event_location
        event.start = start_time
        event.end = end_time
        event.save()
    else:
        msg = ""
        if (error == 1):
            msg = "Your event has no title."
        elif (error == 2):
            msg = "Your event has no description."
        elif (error == 3):
            msg = "Your event has no location."
        elif (error == 4):
            msg = "You did not provide an accurate event start date/end date."
        else:
            msg = "Some data is missing/inaccurate about your event."
        return render(request, 'events/create-event.html', {
            'error_message': msg,
        })

    return HttpResponseRedirect("../")
'''
# Source for forms: https://docs.djangoproject.com/en/3.1/topics/forms/
# create_event is based on the code in the tutorial
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event_title = form.cleaned_data.get('title')
            event_desc = form.cleaned_data.get('desc')
            location = form.cleaned_data.get('location_name')
            address = form.cleaned_data.get('address')
            start_time = form.cleaned_data.get('start')
            end_time = form.cleaned_data.get('end')
            icon = form.cleaned_data.get('icon')

            event = Event(author = request.user, pub_date = timezone.now())
            error = event.exists_required_input(event_title, event_desc, location, address, start_time, end_time) 
            if (error == 0):
                event.title = event_title
                event.desc = event_desc
                event.location_name = location
                event.address = address
                event.start = start_time
                event.end = end_time
                event.icon = icon
                event.save()
            else:
                msg = ""
                if (error == 1):
                    msg = "Your event has no title."
                elif (error == 2):
                    msg = "Your event has no description."
                elif (error == 3):
                    msg = "Your event has no location."
                elif (error == 4):
                    msg = "You did not provide an accurate event start date/end date."
                elif (error == 5):
                    msg = "The provided address is not a valid address."
                else:
                    msg = "Some data is missing/inaccurate about your event."
                return render(request, 'events/create-event2.html', {
                    'error_message': msg, 'form': form
                })
            return HttpResponseRedirect("../")
        else:
            form = EventForm()
    return render(request, 'events/create-event2.html', {'form': form, 'error_message': 'Something went wrong.'})


# Source for search code tutorial: https://www.kobrien.me/blog/post/building-simple-search-django/
# Code used is loosely based on code in tutorial
def search(request):
    query_string = request.GET['searchBar']  # get the contents of the search bar
    event_list = Event.objects.all()  # get all event objects
    found_entries = make_search(query_string, event_list)
    context = {'event_list': found_entries, "search": query_string}
    return render(request, "events/search.html", context)


# RSVP counter
def rsvp(request, event_id):
    action = request.GET['action']
    event = Event.objects.get(pk=event_id)
    if request.user.is_authenticated:  # Prevent unauthenticated users from using the url to affect rsvp
        if action == "rsvp":
            if request.user.username in event.people_going:  # Prevent changing rsvp count through refresh
                event_json = []
                event_json.append({"title": event.title, "address": event.address})
                return render(request, "events/detail.html", {'event': event, 'event_json': event_json})
            else:
                try:
                    event = Event.objects.get(pk=event_id)
                    event.rsvps += 1
                    event.people_going.append(request.user)
                    event.save()
                    event_json = []
                    event_json.append({"title": event.title, "address": event.address})
                except Event.DoesNotExist:
                    raise Http404("Event does not exist")
                event.refresh_from_db()
                return render(request, "events/detail.html", {'event': event, 'event_json': event_json})
        else:
            if request.user.username not in event.people_going:
                event_json = []
                event_json.append({"title": event.title, "address": event.address})
                return render(request, "events/detail.html", {'event': event, 'event_json': event_json})
            else:
                try:
                    event = Event.objects.get(pk=event_id)
                    event.rsvps -= 1
                    event.people_going.remove(request.user.username)
                    event.save()
                    event_json = []
                    event_json.append({"title": event.title, "address": event.address})
                except Event.DoesNotExist:
                    raise Http404("Event does not exist")
                event.refresh_from_db()
                return render(request, "events/detail.html", {'event': event, 'event_json': event_json})
    else:  # Return a blank page with a link to the home page if user is not authenticated
        return HttpResponseNotFound('<h1>Page not found</h1><a href = "/../../../user">Return Home</a>')


def delete(request):
    event_id = request.GET['eventId']
    delete_info = Event.objects.get(id=event_id).delete()

    return render(request, "events/delete.html", {'request': delete_info})


def edit_event(request):
    event_id = request.GET['eventId']
    event = Event.objects.get(id=event_id)
    form = EventForm(initial={'title': event.title, 'desc': event.desc, "location_name": event.location_name,
                              "address": event.address, "start": event.start.isoformat()[:16],
                              "end": event.end.isoformat()[:16], "icon": event.icon})
    context = {"error_message": "", "form": form, "eventId": event_id}
    print(event.end)
    print(event.start)
    return render(request, "events/editEvent.html", {"context": context})


def submit_edit(request):
    success = False
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        event_id = request.POST['event_id']
        if form.is_valid():
            event_title = form.cleaned_data.get('title')
            event_desc = form.cleaned_data.get('desc')
            location = form.cleaned_data.get('location_name')
            address = form.cleaned_data.get('address')
            start_time = form.cleaned_data.get('start')
            end_time = form.cleaned_data.get('end')
            icon = form.cleaned_data.get('icon')

            # event = Event(author = request.user, pub_date = timezone.now())
            event = Event.objects.get(id=event_id)
            error = event.exists_required_input(event_title, event_desc, location, address, start_time, end_time) 
            if (error == 0):
                event.title = event_title
                event.desc = event_desc
                event.location_name = location
                event.address = address
                event.start = start_time
                event.end = end_time
                event.icon = icon
                event.save()
            else:
                msg = ""
                if (error == 1):
                    msg = "Your event has no title."
                elif (error == 2):
                    msg = "Your event has no description."
                elif (error == 3):
                    msg = "Your event has no location."
                elif (error == 4):
                    msg = "You did not provide an accurate event start date/end date."
                elif (error == 5):
                    msg = "The provided address is not a valid address."
                else:
                    msg = "Some data is missing/inaccurate about your event."
                context = {"error_message": msg, "form": form, "eventId": event_id}
                return render(request, 'events/editEvent.html', {"context": context})
            success = True
            return render(request, 'events/submitEdit.html', {"worked": success})
        else:
            form = EventForm()
    return render(request, 'events/submitEdit.html', {"worked": success})

