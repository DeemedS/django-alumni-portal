from .serializers import EventSerializer , ArticleSerializer, JobPostSerializer, ALumniSerializer, CareersSerializer

from django.utils.timezone import now
from events.models import Event
from articles.models import Article
from careers.models import JobPost
from authentication.models import User
from .permissions import IsStaffUser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q

# Create your views here.
class FilteredEventsAPIView(APIView):

    permission_classes = [AllowAny]

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

    permission_classes = [AllowAny]

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
            'student_number': user.student_number,
            'middle_name': user.middle_name,
            'birthday': user.birthday,
            'address': user.address,
            'telephone': user.telephone,
            'mobile': user.mobile,
            'civil_status': user.civil_status,
            'sex' : user.sex,
            'events': user.events,
            'jobs' : user.jobs

        }
        return Response(user_info, status=200)
    else:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
class FilteredJobPostsAPIView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        job_post_filter = request.GET.get('job_post_filter', 'all')
        month = request.GET.get('month')
        year = request.GET.get('year')
        keyword = request.GET.get('keyword', '')
        location = request.GET.get('location', '')
        job_type = request.GET.get('job_type', '')
        
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

        #search by keyword and location
        if keyword:
            job_posts = job_posts.filter(Q(title__icontains=keyword))
        if location:
            job_posts = job_posts.filter(location__icontains=location)

        #filter by jobtype
        if job_type:
            job_posts = job_posts.filter(job_type=job_type)

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size')
        result_page = paginator.paginate_queryset(job_posts, request)
        serializer = JobPostSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
class JobPostDetailView(RetrieveAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    lookup_field = 'id'
class EventsDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
class AlumniListView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, *args, **kwargs):

        users = User.objects.all().order_by("last_name", "first_name")

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)

        # Paginate queryset
        result_page = paginator.paginate_queryset(users, request)

        # Serialize paginated results
        serializer = ALumniSerializer(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    

class CareersListView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, *args, **kwargs):

        careers = JobPost.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)

        # Paginate queryset
        result_page = paginator.paginate_queryset(careers, request)

        # Serialize paginated results
        serializer = CareersSerializer(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)