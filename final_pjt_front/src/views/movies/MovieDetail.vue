<template>
  <div>
    <h2>Movie Detail</h2>
    <div v-if="movie">
      <h3>{{ movie.title }}</h3>
      <p>{{ movie.overview }}</p>
      <hr>
      <h3>Review</h3>
      <ul>
        <li v-for="review in reviews" :key="review.id">{{ review.title }}</li>
      </ul>
      <form>
        <p>title : <input type="text" v-model="review_title"></p>
        <p>내용 : <input type="text" v-model="review_content"></p>
        <button @click.prevent="reviewCreate">+</button>
      </form>
    </div>

  </div>
</template>

<script>
import axios from'axios'

export default {
  name: "MovieDetail",
  data () {
    return {
      id: this.$route.params.movie_id,
      movie: null,
      reviews: null,
      review_title : '',
      review_content : '',
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
    getMovie() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/detail/${this.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.movie = res.data
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
          console.log(res)
          this.reviews = res.data.review_set
        })
        .catch((err) => {
          console.log(err)
        })
    },
    reviewCreate () {
      const reviewItem = {
        title: this.review_title,
        content: this.review_content,
      }
      if (reviewItem.title && reviewItem.content) {
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
  },
  created () {
    this.getMovie()
    this.getReviews()
  },
}
</script>

<style>

</style>