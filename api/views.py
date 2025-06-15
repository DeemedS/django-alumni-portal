import logging
from venv import logger
from django.shortcuts import get_object_or_404
from .serializers import CourseSectionSerializer, CourseWithSectionsSerializer, EventSerializer , ArticleSerializer, JobPostSerializer, ALumniSerializer, RelatedALumniSerializer, StorySerializer, AlumniNetworkSerializer

from django.utils.timezone import now
from events.models import Event
from articles.models import Article
from careers.models import JobPost
from authentication.models import Course, Section, User
from story.models import Stories
from .permissions import IsStaffUser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q
from django.db.models import Count
from datetime import datetime

logger = logging.getLogger(__name__)

# Create your views here.
class FilteredEventsAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            event_filter = request.GET.get('event_filter', 'all')
            search_query = request.GET.get('q')

            try:
                month = int(request.GET.get('month')) if request.GET.get('month') else None
            except ValueError:
                month = None

            try:
                year = int(request.GET.get('year')) if request.GET.get('year') else None
            except ValueError:
                year = None

            try:
                page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
            except ValueError:
                page_size = 10

            is_active = request.GET.get('is_active', 'all')

            events = Event.objects.all().annotate(like_count=Count('liked_by'))

            if search_query:
                events = events.filter(Q(title__icontains=search_query))

            if is_active.lower() in ['true', '1']:
                events = events.filter(is_active=True)
            elif is_active.lower() in ['false', '0']:
                events = events.filter(is_active=False)

            if event_filter == 'upcoming':
                events = events.filter(date__gte=now()).order_by('-date')
            elif event_filter == 'past':
                events = events.filter(date__lt=now()).order_by('-date')
            else:
                events = events.order_by('-date')

            if month:
                events = events.filter(date__month=month)

            if year:
                events = events.filter(date__year=year)

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(events, request)
            serializer = EventSerializer(result_page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.error("Error in FilteredEventsAPIView: %s", str(e), exc_info=True)
            return Response({'error': 'Internal server error'}, status=500)

class FilteredArticlesAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            article_filter = request.GET.get('article_filter', 'all')
            search_query = request.GET.get('q')

            try:
                month = int(request.GET.get('month')) if request.GET.get('month') else None
            except ValueError:
                month = None

            try:
                year = int(request.GET.get('year')) if request.GET.get('year') else None
            except ValueError:
                year = None

            try:
                page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
            except ValueError:
                page_size = 10

            is_active = request.GET.get('is_active', 'all')

            articles = Article.objects.all().annotate(like_count=Count('liked_by'))

            if search_query:
                articles = articles.filter(Q(title__icontains=search_query))

            if is_active.lower() in ['true', '1']:
                articles = articles.filter(is_active=True)
            elif is_active.lower() in ['false', '0']:
                articles = articles.filter(is_active=False)

            if article_filter == 'news':
                articles = articles.filter(category='news').order_by('-date')
            elif article_filter == 'Ann':
                articles = articles.filter(category='Ann').order_by('-date')
            else:
                articles = articles.order_by('-date')

            if month:
                articles = articles.filter(date__month=month)
            if year:
                articles = articles.filter(date__year=year)

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(articles, request)
            serializer = ArticleSerializer(result_page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.error("Error in FilteredArticlesAPIView: %s", str(e), exc_info=True)
            return Response({'error': 'Internal server error'}, status=500)
    

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
            'suffix': user.suffix,
            'profile_image': user.profile_image.url if user.profile_image else None,
            'email': user.email,
            'student_number': user.student_number,
            'middle_name': user.middle_name,
            'birthday': user.birthday,
            'address': user.address,
            'telephone': user.telephone,
            'mobile': user.mobile,
            'civil_status': user.civil_status,
            'sex': user.sex,
            'linkedin_link': user.linkedin_link,
            'facebook_link': user.facebook_link,
            'x_link': user.x_link,
            'events': user.events,
            'jobs': user.jobs,
            'work_experience': user.work_experience,
            'education': user.education,
            'licenses': user.licenses,
            'certifications': user.certifications,
            'course': {
                'id': user.course.id if user.course else None,
                'course_code': user.course.course_code if user.course else None,
                'course_name': user.course.course_name if user.course else None,
            },
            'section': {
                'id': user.section.id if user.section else None,
                'section_code': user.section.section_code if user.section else None,
            },
            'year_graduated': user.year_graduated,
        }

        return Response(user_info, status=200)
    else:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
class FilteredJobPostsAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            keyword = request.GET.get('keyword', '')
            location = request.GET.get('location', '')
            job_type = request.GET.get('job_type', '')
            is_active = request.GET.get('is_active', 'all')
            search_query = request.GET.get('q')

            try:
                page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
            except ValueError:
                page_size = 10

            job_posts = JobPost.objects.all().annotate(
                like_count=Count('liked_by')
            ).order_by('-created_at')

            if search_query:
                job_posts = job_posts.filter(Q(title__icontains=search_query))

            if is_active.lower() in ['true', '1']:
                job_posts = job_posts.filter(is_active=True)
            elif is_active.lower() in ['false', '0']:
                job_posts = job_posts.filter(is_active=False)

            if keyword:
                job_posts = job_posts.filter(Q(title__icontains=keyword))

            if location:
                job_posts = job_posts.filter(location__icontains=location)

            if job_type:
                job_posts = job_posts.filter(job_type=job_type)

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(job_posts, request)
            serializer = JobPostSerializer(result_page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.error("Error in FilteredJobPostsAPIView: %s", str(e), exc_info=True)
            return Response({"error": "Internal server error"}, status=500)
    
class JobPostDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    lookup_field = 'id'
class EventsDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
class AlumniListView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, *args, **kwargs):
        # Get filters from query params
        verification = request.GET.get('verification')
        course_code = request.GET.get('course_code')
        year_graduated = request.GET.get('year_graduated')
        search_query = request.GET.get('search')

        # Start with base queryset
        users = User.objects.all().order_by("last_name", "first_name")

        # Filter: Verification status
        if verification == 'verified':
            users = users.filter(is_active=True)
        elif verification == 'unverified':
            users = users.filter(is_active=False)


        # Filter: Course code (related model)
        if course_code:
            users = users.filter(course__course_code__icontains=course_code)

        # Filter: School year (direct field)
        if year_graduated:
            users = users.filter(year_graduated__icontains=year_graduated)

        # Filter: Basic search on name or email
        if search_query:
            users = users.filter(email__icontains=search_query)

        # Setup pagination
        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)

        result_page = paginator.paginate_queryset(users, request)
        serializer = ALumniSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class RelatedAlumniListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        course_code = request.GET.get('course_code', None)

        base_queryset = User.objects.exclude(Q(first_name="") | Q(last_name=""))

        if course_code:
            users = base_queryset.filter(course__course_code=course_code)\
                .select_related('course')\
                .order_by("?")
        else:
            users = base_queryset.select_related('course')\
            .order_by("?")

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)

        result_page = paginator.paginate_queryset(users, request)
        serializer = RelatedALumniSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class ToggleLikeMixin(APIView):
    permission_classes = [IsAuthenticated]
    model = None

    def post(self, request, pk):
        obj   = get_object_or_404(self.model, pk=pk)
        user  = request.user

        if obj.liked_by.filter(pk=user.pk).exists():
            obj.liked_by.remove(user)
            liked = False
        else:
            obj.liked_by.add(user)
            liked = True

        return Response({
            "liked":       liked,
            "like_count":  obj.liked_by.count()
        })
    
class ToggleArticleLikeAPIView(ToggleLikeMixin):
    model = Article

class ToggleEventLikeAPIView(ToggleLikeMixin):
    model = Event

class ToggleJobLikeAPIView(ToggleLikeMixin):
    model = JobPost


class FilteredStoriesAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        is_active = request.GET.get('is_active', 'all')
        page_size = request.GET.get('page_size') or 10
        search_query = request.GET.get('q')
        
        stories = Stories.objects.all().order_by('-created_at')

        if search_query:
            stories = stories.filter(Q(title__icontains=search_query))

        if is_active.lower() in ['true', '1']:
            stories = stories.filter(is_active=True)
        elif is_active.lower() in ['false', '0']:
            stories = stories.filter(is_active=False)

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(stories, request)
        serializer = StorySerializer(result_page, many=True, context={"request": request})
        
        return paginator.get_paginated_response(serializer.data)
    
class FilteredAlumniAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        is_active = request.GET.get('is_active', 'True')
        page_size = request.GET.get('page_size') or 10
        course_code = request.GET.get('course_code')
        section_code = request.GET.get('section_code')

        if not request.GET.get('year_graduated'):
            current_year = datetime.now().year - 1
            year_graduated = f"{current_year}"
        else:
            year_graduated = request.GET.get('year_graduated')
        
        alumni = User.objects.all().order_by("id")

        if is_active.lower() in ['true', '1']:
            alumni = alumni.filter(is_active=True)
        elif is_active.lower() in ['false', '0']:
            alumni = alumni.filter(is_active=False)

        if course_code:
            alumni = alumni.filter(course__course_code=course_code)

        # # Filter by year_graduated
        if year_graduated:
            alumni = alumni.filter(year_graduated=year_graduated)
        
        if section_code:
            alumni = alumni.filter(section__section_code=section_code)

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(alumni, request)
        serializer = AlumniNetworkSerializer(result_page, many=True, context={"request": request})
        
        return paginator.get_paginated_response(serializer.data)
    
class FilteredCourseSectionAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        page_size = int(request.GET.get('page_size', 10))

        course_name = request.GET.get('course_name')
        course_code = request.GET.get('course_code')
        section_code = request.GET.get('section_code')

        courses = Course.objects.all().order_by("id")

        # Filter by course fields
        if course_name:
            courses = courses.filter(course_name__icontains=course_name)

        if course_code:
            courses = courses.filter(course_code__icontains=course_code)

        # Filter section_code (optional)
        if section_code:
            courses = courses.prefetch_related(
                Prefetch(
                    'sections',
                    queryset=Section.objects.filter(section_code__icontains=section_code),
                    to_attr='filtered_sections'
                )
            )
        else:
            courses = courses.prefetch_related('sections')

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(courses, request)

        serializer = CourseWithSectionsSerializer(result_page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
    
class FilteredCourseSectionWithOnlySectionsAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        page_size = int(request.GET.get('page_size', 10))

        course_name = request.GET.get('course_name')
        course_code = request.GET.get('course_code')
        section_code = request.GET.get('section_code')

        # Filter only courses that have at least one section
        courses = Course.objects.annotate(
            section_count=Count('sections')
        ).filter(section_count__gt=0).order_by("id")

        # Filter by course fields
        if course_name:
            courses = courses.filter(course_name__icontains=course_name)

        if course_code:
            courses = courses.filter(course_code__icontains=course_code)

        # Filter section_code (optional)
        if section_code:
            courses = courses.prefetch_related(
                Prefetch(
                    'sections',
                    queryset=Section.objects.filter(section_code__icontains=section_code),
                    to_attr='filtered_sections'
                )
            )
        else:
            courses = courses.prefetch_related('sections')

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(courses, request)

        serializer = CourseWithSectionsSerializer(result_page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)