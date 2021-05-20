from rest_framework import serializers
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'completed',)

# 댓글 조회
class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)