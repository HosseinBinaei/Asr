from django.shortcuts import render
from core.utils import jalali_now
from django.http import HttpResponseBadRequest
from core.services.elapsed import get_elapsed

def get_time(request):
    now = jalali_now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    context = {'time': formatted_now}
    
    return render(request, 'core/index.html', context)
    

def elapsed_view(request, pk):
    now = jalali_now()
    value = get_elapsed(pk, now)

    if not value:
        return HttpResponseBadRequest("Invalid key")
    context = {'value': value}

    return render(request, 'core/elapsed.html', context)
