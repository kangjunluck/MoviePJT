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
        <div class="col-12 col-md-4">
          <h2>오늘의 랜덤 추천 영화</h2>
          <div v-if="ranMovie">
            <div class="card my-3" style="width:18rem ">
              <img 
                :src="'https://image.tmdb.org/t/p/w500/' + ranMovie.poster_path" 
                class="card-img-top" alt="...">
              <div class="card-body">
                <h3 class="card-title">{{ ranMovie.title }}</h3>
                <button class="btn btn-primary" @click="moveMovieDetail(ranMovie)">Detail</button>
              </div>
            </div>
          </div>
          <h2>최고 평점 영화 Top5</h2>
          <ul class="list">   
            <li class="item fs-3 d-flex justify-content-start" v-for="rankmovie in rankMovies" :key="rankmovie.id">
              <span class="movie-item" @click="moveMovieDetail(rankmovie)">{{ rankmovie.title }}  {{ rankmovie.vote_average }}점</span>
            </li>  
          </ul>
        </div>
        <div class="col-12 col-md-4 ">
          <h2>내가 찜한 영화</h2>
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
.list {
  counter-reset : numbering;
  list-style-type:none;
}
.list .item:before{
  counter-increment : numbering; 
  content : counter(numbering);
  margin-right:10px;
}

.movie-btn {
  margin-left: 10px;
}
.movie-item {
  cursor: pointer;
}
.movie-item:hover {
  border: 2px solid dodgerblue;
}
</style>