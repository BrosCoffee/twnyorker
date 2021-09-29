from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from club.models import Event
from pytz import timezone

@login_required(login_url='/signin')
def calendar(request):
    # TO-DO: Not efficient. Revisit it later
    events = Event.objects.all()
    events_list = []
    for event in events:
        events_list.append({
            'title': event.title,
            'start': event.start_time.astimezone(timezone('Asia/Taipei')).strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.astimezone(timezone('Asia/Taipei')).strftime('%Y-%m-%dT%H:%M:%S'),
        })
    return render(request, 'club/calendar.html', {
        'events_list': events_list,
    })
