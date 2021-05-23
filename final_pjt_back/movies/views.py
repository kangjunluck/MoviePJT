from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Movie, Review
from .serializers import (
    MovieListSerializer, 
    MovieSerializer,     
    ReviewListSerializer, 
    ReviewSerializer)

# Create your views here.

# 전체영화 정보 제공
@api_view(['GET'])
def index(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 단일영화 정보 제공
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 전체 리뷰정보 반환
@api_view(['GET'])
def review_list(request):
    reviews = get_list_or_404(Review)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)


# 리뷰 생성
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data)

# 상세 리뷰 정보, 리뷰 수정, 리뷰 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 리뷰 상세조회
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    # 리뷰 수정
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    # 리뷰 삭제
    else:
        review.delete()
        data = {
            'delete': f'{review_pk}번 리뷰가 삭제되었습니다.'
        }
        return Response(data)


# 영화 좋아요
# @require_POST

# def like(request, review_pk):
#     context = {}
#     if request.user.is_authenticated:
#         review = get_object_or_404(Review, pk=review_pk)
#         user = request.user
        
#         if review.like_users.filter(pk=user.pk).exists():
#             review.like_users.remove(user)
#             context['like'] = False
#         else:
#             review.like_users.add(user)
#             context['like'] = True
        
#         context['counts'] = review.like_users.count()

#     return JsonResponse(context)