from django.shortcuts import render
from events.models import Event


def user_view(request):
    event_list = Event.objects.order_by('-start')[:2]
    event_json = list(event_list.values('title', 'address'))
    context = {'event_list': event_list, 'event_json': event_json}
    return render(request, "webapp/user.html", context)
