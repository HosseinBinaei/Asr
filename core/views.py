from django.shortcuts import render

def get_time(request):
    return render(request, 'core/index.html')