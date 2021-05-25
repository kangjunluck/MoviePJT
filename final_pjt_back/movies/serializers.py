from rest_framework import serializers
from .models import Movie, Review



# 리뷰 전체 조회
class ReviewListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = '__all__'

# 리뷰 상세 조회
class ReviewSerializer(serializers.ModelSerializer):
    
    # movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user', )

# 영화 전체조회
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

# 영화 상세조회
class MovieSerializer(serializers.ModelSerializer):
    review_set = ReviewListSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
