<template>
  <div>
    <h2>Movie Detail</h2>
    <div v-if="movie">
      <h3>{{ movie.title }}</h3>
      <p>{{ movie.overview }}</p>
      <p>이 영화의 평점은 {{ movie_vote }}점</p>
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
                          :show-rating="false">
            </star-rating>
          </div>
          <input type="text" v-model="review.content">
          <button @click.prevent="updateReview(review)">완료</button>
        </div>
        <div v-else>
          {{ review.content }}  평점 : {{ review.person_vote }}점 <br>
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
          console.log(res)
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
          console.log(res)
          this.movie = res.data
          this.likeCnt = res.data.like_users.length
          this.likeUsers = res.data.like_users
          this.base_vote = res.data.vote_average
        })
        .catch((err) => {
          console.log(err)
        })
    },
    updateMovie(movie) {
      const movieItem = {
        ...movie,
        vote_average: this.movie_vote,
      }
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/updatemovie/${this.id}/`,
        data: movieItem,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
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
          let total = 0
          this.reviews.forEach((review)=>{
            total = total + review.person_vote
          })
          this.movie_vote = ((total + parseFloat(this.base_vote)) / (this.reviews.length + 1)).toFixed(1)
          this.updateMovie(this.movie)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    reviewCreate () {
      const reviewItem = {
        content: this.review_content,
        person_vote: this.rating * 2,
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
            this.getReviews()
          })
          .catch((err) => {
            console.log(err)
          })
      }
    },
    updateReview (review) {
      const reviewItem = {
        ...review,
        'person_vote': (review.person_vote)*2,
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
          review.person_vote = review.person_vote * 2
          review.completed = !review.completed
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
          this.getReviews()
        })
        .catch((err) => {
          console.log(err)
        })
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
    this.getMovie()
    this.getReviews()
    this.getUserId()
  },
}
</script>

<style>

</style>