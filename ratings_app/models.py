from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ['user', 'article']
