from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Article, Comment

# 댓글 조회
class CommentListSerializer(serializers.ModelSerializer):

    comment_user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'user',)


class ArticleCutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = ('id', 'content', 'title',)

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentListSerializer(many=True, read_only=True)
    userid = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
