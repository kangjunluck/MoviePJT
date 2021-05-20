from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Article, Comment


class ArticleCutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = ('id', 'content', 'title',)

class ArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = '__all__'

# 댓글 조회
class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)