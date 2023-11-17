from rest_framework import viewsets
from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # Additional logic for average score and user rating

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        user = self.request.user
        article = serializer.validated_data['article']
        score = serializer.validated_data['score']

        rating, created = Rating.objects.update_or_create(
            user=user, article=article, 
            defaults={'score': score}
        )
        serializer.instance = rating

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)
