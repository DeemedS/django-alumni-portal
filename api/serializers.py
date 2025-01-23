from rest_framework import serializers
from events.models import Event
from articles.models import Article
from django.utils.timezone import now
from careers.models import JobPost

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