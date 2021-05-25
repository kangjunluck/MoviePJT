<template>
  <div style="font-family: 'Jua', sans-serif;">    
    <div v-if="movie">
      <!--  -->

      <div class="container">      
        <div class="row">        
          <div class="col-md-3">
            <div>
              <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" height='50%' width='100%'>
            </div>
          </div>
          <div class="col-md-9 " style="border: 4px solid grey;"> 
                      
            <h2> {{ movie.title }} ({{ movie.original_title}})</h2>            
            <hr>
            <h3>줄거리</h3> <br>
            <div class="d-inline-flex p-2 bd-highlight justify-content-center" >{{ movie.overview }} <br></div>
            
            <hr>
            <div class="row p-2" style="">
              <div class="col-md-3 p-2 align-self-center" style="float: none; margin:100 auto;">
                <h3>개봉: {{ movieReleasdate }} 년</h3>
                <h3>러닝 타임: {{ movie.runtime }}분</h3>
              </div>
              <div class="col-md-6 align-self-center" style="">
                <h3>리뷰 평점</h3>
                <h3>영화 평점: {{ movie.vote_average }}점 
                  <star-rating :inline='true'
                              :read-only="true"     
                              :increment="0.1"              
                              :rating="parseFloat(movie.vote_average/2)"
                              :star-size="20"
                              :show-rating="false"
                              active-color="#E50914" 
                              :glow="10"    
                          ></star-rating>
                </h3>
                <h3>User 평점: {{ movie.movie_vote * 2 }}점
                  <star-rating :read-only="true"                                  
                              :increment="0.1"              
                              :rating="movie.movie_vote"
                              :star-size="1"
                              :show-rating="false"   
                              :inline=true    
                              active-color="#E50914"                             
                              :glow="5"      
                          ></star-rating>
                  </h3>             
              </div>
              <div class="col-md-3 align-self-center" style="">
                <h3>영화를 찜한 사람 {{ likeCnt }}명</h3>
                <form id="like-form" style="top: 50%;">
                  <div v-if="!likeUsers.includes(userId)">
                    <button  class="btn btn-link" @click.prevent="onLike(movie)">
                      <i class="fas fa-heart fa-3x" style="color:white;"></i>
                    </button>
                  </div>
                  <div v-else>
                    <button  class="btn btn-link" @click.prevent="onLike(movie)">
                      <i class="fas fa-heart fa-3x" style="color:crimson;"></i>
                    </button>
                  </div>      
                </form>
              </div>
            </div>
          </div>
        </div>
        <br>
        <h1>Trailer</h1>  
        <div class="embed-responsive embed-responsive-16by9" style="">
          <iframe   
            class="embed-responsive-item"
            :src= "videoUrl"
            frameborder="0" 
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen
            style="allign: middle;"
          ></iframe>
        </div>
      </div>
      <!--  --> 

      <div class="container">
        <hr>  
        <h3>유저 리뷰</h3>
        <ul>
          <div v-for="review in reviews" :key="review.id">
            <div v-if="review.completed">
              <div>
                <star-rating v-model="review.person_vote" 
                              v-bind:star-size="5"
                              :show-rating="false"
                              :inline=true
                              active-color="#E50914"                           
                              >
                </star-rating>
              </div>
              <input type="text" v-model="review.content">              
              <button @click.prevent="updateReview(review)" class="btn btn-danger">수정완료</button>
              
            </div>
            <div v-else>
              <h2>{{ review.content }}                               
              </h2>
                  <star-rating :read-only="true"                                  
                               :increment="0.1"              
                               :rating="review.person_vote"
                               :show-rating="false"   
                               :inline=true    
                               :glow="5"
                               v-bind:star-size="1"
                               active-color="#E50914"></star-rating>
                  {{ review.person_vote*2 }}점
                <div class="inline" v-if="review.user === userId">
                  <button @click.prevent="updateReview(review)" class="btn btn-secondary">수정</button>
                  <button @click.prevent="deleteReview(review), reviewExist=false" class="btn btn-secondary">삭제</button>
                </div>                             
            </div>
            <hr>                        
          </div>
        </ul>
        <hr>
        <h3>리뷰 작성</h3>        
        <form v-if="!reviewExist">        
          <h3>
            <input type="text" v-model="review_content" placeholder="리뷰내용을 입력해주세요">
            <button @click.prevent="reviewCreate" class="btn btn-danger">제출</button>
          </h3>
          <div>
            <star-rating v-model="rating" 
                        v-bind:star-size="5"
                        :show-rating="false"
                        :increment="1"
                        active-color="#E50914"
                        :inline=true
                        >
            </star-rating>
            <span>{{ rating * 2 }} 점</span>
          </div>
        </form>
        <div v-else>
          <h2 style="color:red">이미 리뷰를 작성했습니다!</h2> 
        </div>
             
      </div>
      
    </div>

  </div>
</template>

<script type="text/javascript">   
import {StarRating} from 'vue-rate-it';
import axios from'axios'


export default {
  components: {
    StarRating,
  },
  name: "MovieDetail",
  data () {
    return {
      id: this.$route.params.movie_id,
      userId: null,
      userName: '',
      movie: null,
      movieReleasdate: null,
      base_vote: null,
      reviews: null,
      review_content : '',
      rating: 3,
      movie_vote: null,

      reviewExist: false,
      likeCnt: null,
      likeUsers: [],
      baseUrl: 'https://www.youtube.com/embed/',
      videoUrl: ''
    }
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getUserId () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/accounts/userid/',
        headers: this.setToken()
      })
        .then((res) => {
          this.userId = res.data.userid
          this.userName = res.data.username
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getMovie() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/detail/${this.id}/`,
        headers: this.setToken()
      })
        .then((res) => {          
          this.movie = res.data          
          this.movieReleasdate = res.data.release_date.substring(0,4)          
          this.videoUrl = this.baseUrl + res.data.video
          this.likeCnt = res.data.like_users.length
          this.likeUsers = res.data.like_users
          this.base_vote = res.data.vote_average
        })
        .catch((err) => {
          console.log(err)
        })
    },
    updateMovie(movie) {
      console.log(this.movie_vote)
      const movieItem = {
        ...movie,
        movie_vote: this.movie_vote,
      }
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/updatemovie/${this.id}/`,
        data: movieItem,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.getMovie()
          this.getReviews()
        })
        .catch((err) => {          
          console.log(err)
        })
    },

    getReviews() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/detail/${this.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          this.reviews = res.data.review_set
          console.log(this.userId, this.reviews, this.reviews.user)
          this.reviews.forEach(element=>{            
            if (this.userId == element.user) {
              this.reviewExist = true
            }
          })          
          
        })
        .catch((err) => {
          console.log(err)
        })
    },
    reviewCreate () {
      const reviewItem = {
        content: this.review_content,
        person_vote: this.rating,
      }
      if (reviewItem.content && reviewItem.person_vote) {
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/${this.movie.id}/review/`,
          data: reviewItem,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            const myPromise = new Promise((resolve, reject) => {
            axios({
              method: 'get',
              url: `http://127.0.0.1:8000/movies/detail/${this.id}/`,
              headers: this.setToken()
            })
              .then((res) => {
                console.log(res)
                resolve()
                this.reviews = res.data.review_set
              })
              .catch((err) => {
                console.log(err)
                reject()
              })
            })
            myPromise.then(()=>{
                this.calculateVote()
              })
          })
          .catch((err) => {
            console.log(err)
          })
      }
    },
    updateReview (review) {
      const reviewItem = {
        ...review,
        'person_vote': review.person_vote,
        'content': review.content,
        'completed': !review.completed,
      }
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/reviewupdate/${review.id}/`,
        data: reviewItem,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          const myPromise = new Promise((resolve, reject) => {
            axios({
              method: 'get',
              url: `http://127.0.0.1:8000/movies/detail/${this.id}/`,
              headers: this.setToken()
            })
              .then((res) => {
                console.log(res)
                resolve()
                this.reviews = res.data.review_set
              })
              .catch((err) => {
                console.log(err)
                reject()
              })
            })
            myPromise.then(()=>{
              this.calculateVote()
              })
        })
        .catch((err) => {
          console.log(err)
        })
    },
    deleteReview (review) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/movies/reviewupdate/${review.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)          
          const myPromise = new Promise((resolve, reject) => {
            axios({
              method: 'get',
              url: `http://127.0.0.1:8000/movies/detail/${this.id}/`,
              headers: this.setToken()
            })
              .then((res) => {
                console.log(res)
                resolve()                
                this.reviews = res.data.review_set
              })
              .catch((err) => {
                console.log(err)
                reject()
              })
            })
          myPromise.then(()=>{
            this.calculateVote()
          })
        })
        .catch((err) => {
          console.log(err)
        })
    },
    calculateVote () {
      let total = 0
      console.log(this.reviews)
      if (this.reviews.length !== 0) {
        this.reviews.forEach((review)=>{
          total = total + review.person_vote
        })
        this.movie_vote = ((total) / (this.reviews.length)).toFixed(1)
      } else {
        this.movie_vote = 0
      }
      this.updateMovie(this.movie)
    },


    onLike (movie) {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${movie.id}/like/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.likeCnt = res.data.counts
          this.getMovie()
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },
  created () {
    this.getUserId()
    this.getMovie()
    this.getReviews()
  },
}
</script>

<style>

</style>