from rest_framework import serializers
from events.models import Event
from articles.models import Article
from django.utils.timezone import now
from careers.models import JobPost
from authentication.models import User

class EventSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_status(self, obj):
        return "Upcoming Event" if obj.date >= now() else "Past Event"
    
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

class JobPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobPost
        fields = '__all__'

class ALumniSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(source="course.course_code", read_only=True)
    section_code = serializers.CharField(source="section.section_code", read_only=True)
    class Meta:
        model = User
        fields = ['id', 'is_active', 'email', 'first_name', 'last_name', 'middle_name', 'mobile', 'course_code', 'section_code', 'school_year']
