<template>
  <div class="home">
    Home
    <div class="container">
      <div class="row">
        <div class="col-4">
          <h3>여기는 나닮배</h3>
        </div>
        <div class="col-4">
          <h3>오늘의 랜덤 추천 영화</h3>
          <div v-if="ranMovie">
            {{ ranMovie.title }}
          </div>
          <h3>최고 평점 영화 top5</h3>
          <div v-for="rankmovie in rankMovies" :key="rankmovie.id">
            <p>{{ rankmovie.title }}</p>
            <p>{{ rankmovie.vote_average }}</p>
          </div>
        </div>
        <div class="col-4">
          <h3>내가 찜한 영화</h3>
          <div v-for="likemovie in likeMovies" :key="likemovie.id">
            <h4>{{ likemovie.title }}</h4>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from'axios'
import _ from 'lodash'

export default {
  name: 'Home',
  data () {
    return {
      userId: null,
      likeMovies: [],

      movies: [],
      ranMovie: null,

      rankMovies: [],
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
          this.likeMovies = res.data.likeMovies
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getMovies () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/',
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.movies = res.data
          this.randomMovie()
        })
        .catch((err) => {
          console.log(err)
        })
    },
    randomMovie () {
      this.ranMovie =_.sampleSize(this.movies, 1)[0]
    },
    rankingMovie () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/rankmovie/',
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.rankMovies = res.data.movies
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },
  created () {
    this.getUserId()
    this.getMovies()
    this.rankingMovie()
  },
}
</script>
