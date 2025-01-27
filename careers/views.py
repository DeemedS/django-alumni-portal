from django.shortcuts import render
from .models import JobPost

# Create your views here.

def careers(request):
    return render(request, 'careers/careers.html')

def career_page(request, id):
    job = JobPost.objects.get(id=id)
    return render(request, 'careers/career_page.html', {'job': job})