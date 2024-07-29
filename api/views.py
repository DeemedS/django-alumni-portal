from .serializers import EventSerializer , ArticleSerializer

from django.utils.timezone import now
from events.models import Event
from articles.models import Article

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class FilteredEventsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        event_filter = request.GET.get('event_filter', 'all')
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        events = Event.objects.all()

        if event_filter == 'upcoming':
            events = events.filter(date__gte=now()).order_by('-date')
        elif event_filter == 'past':
            events = events.filter(date__lt=now()).order_by('-date')
        else:
            events = events.order_by('-date')
        
        if month and month != 0:
            events = events.filter(date__month=month)

        if year:
            events = events.filter(date__year=year)

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size')
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    

class FilteredArticlesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        article_filter = request.GET.get('article_filter', 'all')
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        articles = Article.objects.all()

        if article_filter == 'upcoming':
            articles = articles.filter(date__gte=now()).order_by('-date')
        elif article_filter == 'past':
            articles = articles.filter(date__lt=now()).order_by('-date')
        else:
            articles = articles.order_by('-date')
        
        if month and month != 0:
            articles = articles.filter(date__month=month)

        if year:
            articles = articles.filter(date__year=year)

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size')
        result_page = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)