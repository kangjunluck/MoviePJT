from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Article, Comment

# 댓글 조회
class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)

class ArticleCutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = ('id', 'content', 'title',)

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentListSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
