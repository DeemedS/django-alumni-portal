from .serializers import EventSerializer , ArticleSerializer, JobPostSerializer

from django.utils.timezone import now
from events.models import Event
from articles.models import Article
from careers.models import JobPost

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView

from rest_framework.decorators import api_view
from rest_framework.response import Response


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

        if article_filter == 'news':
            articles = articles.filter(category='news').order_by('-date')
        elif article_filter == 'Ann':
            articles = articles.filter(category='Ann').order_by('-date')
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
    

@api_view(['GET'])
def get_user_info(request):
    """
    API View to get the user's first name and last name.
    """
    if request.user.is_authenticated:

        user = request.user

        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'student_number': user.student_number
        }
        return Response(user_info, status=200)
    else:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
class FilteredJobPostsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        job_post_filter = request.GET.get('job_post_filter', 'all')
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        job_posts = JobPost.objects.all()

        if job_post_filter == 'internship':
            job_posts = job_posts.filter(category='internship').order_by('-created_at')
        elif job_post_filter == 'job':
            job_posts = job_posts.filter(category='job').order_by('-created_at')
        else:
            job_posts = job_posts.order_by('-created_at')
        
        if month and month != 0:
            job_posts = job_posts.filter(date__month=month)

        if year:
            job_posts = job_posts.filter(date__year=year)

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size')
        result_page = paginator.paginate_queryset(job_posts, request)
        serializer = JobPostSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
class JobPostDetailView(RetrieveAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    lookup_field = 'id'