import calendar
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import *
from .utils import Calendar
from .forms import EventForm

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = format_html(html_cal)
        context['calendario'] = html_cal
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        wa = workteam_activity.objects.all()
        challenge = Challenge.objects.last()
        events = Event.objects.filter(grade=challenge.grade)
        activities = Activity.objects.all().select_related('event')
        event_dict = {}
        for event in events:
            activities_list = []
            activities_list = [act.workteam_activity_set.first() for act in event.activity_set.all()]
            # for act in event.activity_set.all():
            #     print("*"*50)
            #     acti = act.workteam_activity_set.first()
            #     print(acti)
            #     print(acti.state)
            #     print(acti.activity)
            #     print("*"*50)
            event_dict[event] = activities_list

        act = self.request.GET.get('activity')

        if act:
            str_activity = act.split('-')[1]
            wact = workteam_activity.objects.get(id=int(str_activity))
            if wact.state:
                wact.state = False
            else:
                wact.state = True

            wact.save()


        context['events'] = event_dict
        return context

    # def get(self, request):
    #     activity =  request.GET.get('activity')
    #     print(activity)
    #     return render(request, 'cal/calendar.html')

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})