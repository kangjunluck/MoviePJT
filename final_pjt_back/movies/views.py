from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
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

import json
import requests
from collections import OrderedDict

from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .forms import PostForm
from .models import Post


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
    # reviews = get_list_or_404(Review, movie_id=movie_pk)
    # total = 0
    # num = len(reviews) 
    # for rev in reviews:
    #     total += rev.person_vote
    # if total != 0:
    #     avg = round(total / num, 1)
    # else:
    #     avg = 0
    # print(avg)
    # serializer.data["avg"] = avg
    # print(serializer.data)
    return Response(serializer.data)
# movie 데이터 _수정
@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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

# 리뷰 수정, 리뷰 삭제
@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 리뷰 수정
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        print(serializer)
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
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like(request, movie_pk):
    context = {}
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            context['like'] = False
        else:
            movie.like_users.add(user)
            context['like'] = True
        
        context['counts'] = movie.like_users.count()

    return Response(context)

# 평점 상위 10개 영화 가져오기
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def rankmovie(request):
    movies = list(Movie.objects.order_by('-vote_average')[:5].values())
    context = {
        'movies': movies
    }
    return Response(context)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def find_actor(request):
    # 유명인 찾기
    client_id = "QqPmapr9zfg_3Fi05iIn"
    client_secret = "awJxrIA5Np"
    # url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
    url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
    files = {'image': open('./movies/민평홍.jpg', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code

    response_data = json.loads(response.text)
    if(rescode==200):
        ordered_data = sorted(response_data["faces"], key=lambda x:x['celebrity']['confidence'], reverse=True)
        actor_name = ordered_data[0]['celebrity']['value']
        actor_confidence = ordered_data[0]['celebrity']['confidence']
        print (response_data['faces'])
        apikey = '1f4ac8ec8d56852461c1bf865cdc05a1'
        movie_list = range(1)
        mylist = []
        cnt = 1
        file_data = OrderedDict()
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json"
        param = {
            'key' : apikey,
            'peopleNm' : actor_name,    
        }
        r = requests.get(url, params= param)
        data = json.loads(r.text)
        movie_list = []
        for person in data['peopleListResult']['peopleList']:
            if person['repRoleNm'] == '배우':
                listmovies = list(map(str,person['filmoNames'].split('|')))
                movie_list += listmovies
        # print(movies)
        context = {
            'movie_list': movie_list,
            'actor_name': actor_name,
            'actor_confidence': actor_confidence
        }
        print(context)
        return Response(context)
    else:
        print("Error Code:" + rescode)
        return Response("Error Code:" + rescode)



# 유저이미지 올리기
@require_http_methods(['GET', 'POST'])
def uploadimg(request):
    if request.method == 'POST':
        print('왓니?')
        form = PostForm(request.POST, request.FILES)
        print(request.FILES)
        print(form)
        print('여기는?')
        if form.is_valid():            
            form.save()
            
            return redirect('http://localhost:8080/similar')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'imgupload.html', context)


def upload(request):
    return render(request, 'imgupload.html')