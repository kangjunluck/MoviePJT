<template>
  <div>    
    <div v-if="movie">
      <!--  -->
      <h1>
      {{ movie.title }}
      </h1>
      <div class="row p-5">        
        <div class="col-3">
          <div>
            <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" height='50%' width='100%'>
          </div>
        </div>
        <div class="col-9 " style="border: 4px solid grey;"> 
          <h3>Original Title: </h3>
          <h2>{{ movie.original_title}}</h2>            
          <hr>
          <h3>줄거리</h3> <br>
          <div class="d-inline-flex p-2 bd-highlight justify-content-center" >{{ movie.overview }} <br></div>
          
          <hr>
          <div class="row p-2">
            <div class="col-3 p-2" style="border: 2px solid grey;">
              <p>개봉: {{ movieReleasdate }} 년</p>
              <p>러닝 타임: {{ movie.runtime }}분</p>
            </div>
            <div class="col-6 overflow-auto" style="border: 2px solid grey;">
              <h3>리뷰 평점</h3>
              <h3>영화 평점: {{ movie.vote_average }}점 
                <star-rating :inline='true'
                             :read-only="true"     
                             :increment="0.1"              
                             :rating="parseFloat(movie.vote_average/2)"
                             :star-size="20"
                             :show-rating="false"     
                        ></star-rating>
              </h3>
              <h3>User 평점: {{ movie.movie_vote * 2 }}점
                <star-rating :read-only="true"                                  
                             :increment="0.1"              
                             :rating="movie.movie_vote"
                             :star-size="1"
                             :show-rating="false"   
                             :inline=true          
                        ></star-rating>
                </h3>             
            </div>
            <div class="col-3" style="border: 2px solid grey;">
              <p>이 영화를 찜한 사람은 {{ likeCnt }}명</p>
              <form id="like-form">
                <div v-if="!likeUsers.includes(userId)">
                  <button  class="btn btn-link" @click.prevent="onLike(movie)">
                    <i class="fas fa-heart fa-lg" style="color:white;"></i>
                  </button>
                </div>
                <div v-else>
                  <button  class="btn btn-link" @click.prevent="onLike(movie)">
                    <i class="fas fa-heart fa-lg" style="color:crimson;"></i>
                  </button>
                </div>      
              </form>
            </div>
          </div>
        </div>

        <div class="embed-responsive embed-responsive-16by9" >
          <iframe   
            class="embed-responsive-item"
            :src= "videoUrl"
            frameborder="0" 
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen
            style="allign: middle; display:block; width:50vw; height: 50vh"
          ></iframe>
        </div>
      </div>
      <!--  --> 

      <form id="like-form">
        <div v-if="!likeUsers.includes(userId)">
          <button  class="btn btn-link" @click.prevent="onLike(movie)">
            <i class="fas fa-heart fa-lg" style="color:black;"></i>
          </button>
        </div>
        <div v-else>
          <button  class="btn btn-link" @click.prevent="onLike(movie)">
            <i class="fas fa-heart fa-lg" style="color:crimson;"></i>
          </button>
        </div>      
      </form>
      <hr>
      <h3>Review</h3>
      <li v-for="review in reviews" :key="review.id">
        <div v-if="review.completed">
          <div>
            <star-rating v-model="review.person_vote" 
                          v-bind:star-size="5"
                          :show-rating="false"                          
                          >
            </star-rating>
          </div>
          <input type="text" v-model="review.content">
          <button @click.prevent="updateReview(review)">완료</button>
        </div>
        <div v-else>
          {{ review.content }}  평점 : {{ review.person_vote*2 }}점 <br>
          <div v-if="review.user === userId">
            <button @click.prevent="updateReview(review)">수정</button>
          </div>
        </div>
        <div v-if="review.user === userId">
          <button @click.prevent="deleteReview(review)">삭제</button>
        </div>
      </li>
      <hr>

        <form v-if="!reviewExist">        
          <div>
            <star-rating v-model="rating" 
                        v-bind:star-size="5"
                        :show-rating="false"
                        
                        >
            </star-rating>
            <span>{{ rating * 2 }}</span>
          </div>
          <p>내용 : <input type="text" v-model="review_content"></p>
          <button @click.prevent="reviewCreate">+</button>
        </form>        
      
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