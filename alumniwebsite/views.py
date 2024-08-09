from django.shortcuts import render
from .forms import FormWithCaptcha
from articles.models import Article
from django.db.models.signals import post_delete
from django.dispatch import receiver

def home(request):
    context = {'form' : FormWithCaptcha()}
    return render(request, 'home/home.html', context)
