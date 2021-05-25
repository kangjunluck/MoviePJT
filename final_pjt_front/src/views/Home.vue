<template>
  <div class="home" style="font-family: 'Jua', sans-serif;">
    Home
    <div class="container">
      <div class="row">
        <div class="col-12 col-md-4">
          <h2>여기는 나닮배</h2>
          <div class="border-right-danger">
          </div>
        </div>
        <div class="col-12 col-md-4 ">
          <h2>오늘의 랜덤 추천 영화</h2>
          <div v-if="ranMovie">
            <div class="card my-3" style="">
              <img 
                :src="'https://image.tmdb.org/t/p/w500/' + ranMovie.poster_path" 
                class="card-img-top" alt="No image">
              <div class="card-body">
                <h3 class="card-title">{{ ranMovie.title }}</h3>
                <button class="btn btn-primary" @click="moveMovieDetail(ranMovie)">Detail</button>
              </div>
            </div>
          </div>
          <h2>최고 평점 영화 Top5</h2>        
          <div class="list-group">
            <div v-for="rankmovie in rankMovies" :key="rankmovie.id">
              <button type="button" class="list-group-item list-group-item-action" aria-current="true" data-bs-toggle="offcanvas" :data-bs-target="'#offcanvasBottom' + rankmovie.id" aria-controls="offcanvasBottom">
                <span>{{ rankmovie.title }}  {{ rankmovie.vote_average }}점</span>
              </button>
              <div class="offcanvas offcanvas-bottom" style="min-height: 25rem;" tabindex="-1" :id="'offcanvasBottom' + rankmovie.id" aria-labelledby="offcanvasBottomLabel">
                <div class="offcanvas-header">
                  <h3 class="offcanvas-title" id="offcanvasBottomLabel">{{ rankmovie.title }}</h3>
                  <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <h4>평점 : {{ rankmovie.vote_average }}점  상영시간 : {{ rankmovie.runtime }}분</h4>
                <div class="offcanvas-body small fs-4">
                  {{rankmovie.overview}}
                </div>
              </div>

            </div>
          </div>
        </div>
        <div class="col-12 col-md-4 ">
          <h2>내가 찜한 영화</h2>
          <vue-carousel :data="data"></vue-carousel>
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
  components: {
  },
  data () {
    return {
      userId: null,
      likeMovies: null,

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
    moveMovieDetail (movie) {
      this.$router.push({ 
        name: "MovieDetail",
        params: {
          movie_id: movie.id,
        }
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

<style scoped>
</style>