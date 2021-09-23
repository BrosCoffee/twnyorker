from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin')
def calendar(request):
    return render(request, 'club/calendar.html', {})
