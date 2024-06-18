from django.shortcuts import render

# Create your views here.
def portal(request):
    return render(request, 'portal.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'signup.html')

def faculty(request):
    return render(request, 'faculty.html')
