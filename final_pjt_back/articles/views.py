from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ArticleSerializer, CommentListSerializer, ArticleCutSerializer
from .models import Article, Comment


@api_view(['GET', 'POST'])
# JWT 을 활용한 인증을 할 때 JWT 자체를 인증 여부와 상관 없이 JWT가 유효한지 여부만 파악
@authentication_classes([JSONWebTokenAuthentication])
# 인증이 되지 않은 상태로 요청이 오면
# "자격 인증 데이터"가 제공되지 않았습니다와 같은 메세지를 응답함
@permission_classes([IsAuthenticated])
def article_list_create(request):
    if request.method == 'GET':
        # articles = Article.objects.all()
        serializer = ArticleSerializer(request.user.articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleCutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['PUT', 'DELETE', 'GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def article_update_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 1. 해당 article의 유저가 아닌 경우 article를 수정하거나 삭제하지 못하게 설정
    if not request.user.articles.filter(pk=article_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


    if request.method == 'PUT':
        serializer = ArticleCutSerializer(article, data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response({ 'id': article_pk }, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)



# 댓글 생성
@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data)


# 전체 댓글 조회
@api_view(['GET'])
def comment_list(request):
    comments = get_list_or_404(Comment)
    serializer = CommentListSerializer(comments, many=True)
    return Response(serializer.data)
    