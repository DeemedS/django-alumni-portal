from django.shortcuts import render

# Create your views here.
def story(request):
    return render(request, 'story/story.html', {})

def story_page(request):
    return render(request, 'story/story_page.html', {})