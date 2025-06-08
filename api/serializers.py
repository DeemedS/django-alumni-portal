from rest_framework import serializers
from events.models import Event
from articles.models import Article
from django.utils.timezone import now
from careers.models import JobPost
from authentication.models import User
from story.models import Stories

class EventSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField()
    is_liked   = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'status', 'title', 'body', 'slug', 'banner', 'thumbnail', 'date',
            'created_at', 'is_active', 'like_count', 'is_liked'
        ]

    def get_status(self, obj):
        from django.utils.timezone import now
        return "Upcoming Event" if obj.date >= now() else "Past Event"
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.liked_by.filter(pk=user.pk).exists()
        return False
    
class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    is_liked   = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'body', 'slug', 'banner', 'thumbnail', 'author',
            'date', 'created_at', 'featured', 'is_active', 'order', 'category',
            'like_count', 'is_liked'
        ]

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.liked_by.filter(pk=user.pk).exists()
        return False
class JobPostSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    is_liked   = serializers.SerializerMethodField()

    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'company', 'location', 'job_type', 'description',
            'responsibilities', 'qualifications', 'benefits', 'salary',
            'created_at', 'is_active', 'like_count', 'is_liked'
        ]
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.liked_by.filter(pk=user.pk).exists()
        return False

class ALumniSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(source="course.course_code", read_only=True)
    section_code = serializers.CharField(source="section.section_code", read_only=True)
    class Meta:
        model = User
        fields = ['id', 'is_active', 'email', 'first_name', 'last_name', 'middle_name', 'mobile', 'course_code', 'section_code', 'school_year']

class RelatedALumniSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(source="course.course_code", read_only=True)
    section_code = serializers.CharField(source="section.section_code", read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'course_code', 'section_code', 'school_year', 'work_experience', 'profile_image']

class StorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Stories
        fields = [
            'id', 'title' , 'body', 'banner', 'thumbnail', 'created_at', 'is_active'   
        ]

class AlumniNetworkSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source="course.course_code", read_only=True)
    section_code = serializers.CharField(source="section.section_code", read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'course_code', 'section_code', 'school_year', 'work_experience', 'profile_image',
                'facebook_link', "x_link", "linkedin_link"]