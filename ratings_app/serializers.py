from rest_framework import serializers
from .models import Article, Rating
from django.db.models import Avg
        
class ArticleSerializer(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'text', 'average_score', 'user_rating']

    def get_average_score(self, obj):
        ratings = Rating.objects.filter(article=obj)
        if ratings:
            return ratings.aggregate(Avg('score'))['score__avg']
        return 0

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                rating = Rating.objects.get(article=obj, user=user)
                return rating.score
            except Rating.DoesNotExist:
                return 'Not rated'
        return 'Register to see your rating'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'article', 'score']
