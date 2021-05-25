<template>
  <div>
    <h2>Movie Detail</h2>
    <div v-if="movie">
      <!--  -->
      <!-- <div class="row p-2">
        <div class="col-3">
          <div>
            <img src="{{ movie.poster_path }}" alt="{{ movie.title }}_poster" width='100%'>
          </div>
        </div>
        <div class="col-9">
          <h3>
          {{ movie.title }}
          </h3>
          <h5>
          {{ movie.overview }}
          </h5>
        </div>
      </div> -->
      <!--  -->
      <h3>{{ movie.title }}</h3>
      <p>{{ movie.overview }}</p>

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
      <p>이 영화의 평점은 {{ movie.vote_average }}점</p>
      <p>유저들의 평점은 {{ movie.movie_vote * 2 }}점</p>
      <p>이 영화를 좋아하는 사람은 {{ likeCnt }}명 </p>
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
      <form>
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
      base_vote: null,
      reviews: null,
      review_content : '',
      rating: 3,
      movie_vote: null,

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
          console.log('여기?')
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