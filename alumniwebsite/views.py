from django.shortcuts import render
from .forms import FormWithCaptcha

def home(request):
    context = {'form' : FormWithCaptcha()}
    return render(request, 'home/home.html', context)