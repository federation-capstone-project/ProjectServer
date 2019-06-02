from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {}
    return render(request, 'frontend/index.html', context)

def record(request):
    context = {}
    return render(request, 'frontend/record.html', context)
