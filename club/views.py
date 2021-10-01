from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from club.models import Event
from account.models import SiteUser
from pytz import timezone
from datetime import datetime

@login_required(login_url='/signin')
def calendar(request):
    asia = timezone('Asia/Taipei')
    if request.is_ajax():
        event_pk = request.POST.get('eventPk', None)
        user_pk = request.POST.get('userPk', None)
        selected_event = Event.objects.filter(pk=event_pk).first() if event_pk else None
        # TO-DO: User restriction. eq: Youth or Adult
        user = SiteUser.objects.filter(pk=user_pk).first() if user_pk else None
        print('user:',user)
        time_now_str = request.POST.get('timeNow', None)
        try:
            # time_now_str format eq: Fri Oct 01 2021 12:12:38 GMT+0800 (Taipei Standard Time)
            time_now_str_front, time_now_str_end = time_now_str.split(' (')
            time_now = datetime.strptime(time_now_str_front, '%a %b %d %Y %H:%M:%S %Z%z')
            if selected_event:
                host = selected_event.host.get_full_name()
                start_time = selected_event.start_time.astimezone(asia).strftime('%I:%M %p')
                end_time = selected_event.end_time.astimezone(asia).strftime('%I:%M %p')
                if time_now > selected_event.signup_deadline.astimezone(asia):
                    expire = True
                else:
                    expire = False
                max_participants = selected_event.max_participants
                num_participants = len(selected_event.members.all())
                note = selected_event.note
                signup_deadline = selected_event.signup_deadline.astimezone(asia).strftime('%Y/%m/%d %I:%M %p') if selected_event.signup_deadline else None
                return JsonResponse({
                    'expire': expire,
                    'host': host,
                    'start_time': start_time,
                    'end_time': end_time,
                    'max_participants': max_participants,
                    'num_participants': num_participants,
                    'note': note,
                    'signup_deadline': signup_deadline,
                }, safe=False)
        except:
            print('something wrong!')
            print('time_now_str:',time_now_str)
    # TO-DO: Not efficient. Revisit it later
    events = Event.objects.all()
    events_list = []
    for event in events:
        events_list.append({
            'title': event.title,
            'eventPk': event.pk,
            'start': event.start_time.astimezone(asia).strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.astimezone(asia).strftime('%Y-%m-%dT%H:%M:%S'),
        })
    return render(request, 'club/calendar.html', {
        'events_list': events_list,
    })
