from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
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
                expired = True if time_now > selected_event.signup_deadline.astimezone(asia) else False
                booked = True if user in selected_event.members.all() else None
                host = selected_event.host.get_full_name()
                start_time = selected_event.start_time.astimezone(asia).strftime('%-I:%M %p')
                end_time = selected_event.end_time.astimezone(asia).strftime('%-I:%M %p')
                max_participants = selected_event.max_participants
                num_participants = len(selected_event.members.all())
                age_restrictions = selected_event.age_restrictions
                if age_restrictions == 'AD':
                    age_restrictions_pass = True if not user.is_under_age() else False
                elif age_restrictions == 'YO':
                    age_restrictions_pass = True if user.is_under_age() else False
                else: # age_restrictions == 'NR'
                    age_restrictions_pass = True
                note = selected_event.note
                signup_deadline = selected_event.signup_deadline.astimezone(asia).strftime('%Y/%m/%d %-I:%M %p') if selected_event.signup_deadline else None
                return JsonResponse({
                    'expired': expired,
                    'booked': booked,
                    'host': host,
                    'start_time': start_time,
                    'end_time': end_time,
                    'max_participants': max_participants,
                    'num_participants': num_participants,
                    'age_restrictions': age_restrictions,
                    'age_restrictions_pass': age_restrictions_pass,
                    'note': note,
                    'signup_deadline': signup_deadline,
                }, safe=False)
        except:
            messages.error(request, 'There are some errors, please contact Raymond.')
    # TO-DO: Not efficient. Revisit it later
    events = Event.objects.all()
    events_list = []
    for event in events:
        if event.age_restrictions == 'AD':
            event_color = '#fc0d15'
        elif event.age_restrictions == 'YO':
            event_color = '#8132a8'
        else:
            event_color = ''
        events_list.append({
            'title': event.title,
            'eventPk': event.pk,
            'start': event.start_time.astimezone(asia).strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.astimezone(asia).strftime('%Y-%m-%dT%H:%M:%S'),
            'color': event_color,
        })
    if request.method == 'POST':
        event_action = request.POST.get('eventAction')
        selected_user_pk = request.POST.get('selectedUser', None)
        selected_event_pk = request.POST.get('selectedEvent', None)
        try:
            selected_user = SiteUser.objects.get(pk=selected_user_pk)
            selected_event = Event.objects.get(pk=selected_event_pk)
            if event_action == 'bookEvent':
                selected_event.members.add(selected_user)
                selected_event.save()
                messages.success(request, 'Successfully booked ' + selected_event.title)
            elif event_action == 'cancelEvent':
                selected_event.members.remove(selected_user)
                selected_event.save()
                messages.success(request, 'Successfully canceled ' + selected_event.title)
        except ObjectDoesNotExist:
            messages.error(request, 'ObjectDoesNotExist errors, please contact Raymond.')
        except:
            messages.error(request, 'There are some errors, please contact Raymond.')
    return render(request, 'club/calendar.html', {
        'events_list': events_list,
    })
