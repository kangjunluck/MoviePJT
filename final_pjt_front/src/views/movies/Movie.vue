<template>
  <div class="home">
    <h1>Movie</h1>
    <div class='container'>
      <div class="row">
        <div class="col-2">
          <div class="btn btn-primary" @click.prevent="actionFilter">액션</div>
          <div class="btn btn-primary">SF</div>
        </div>
        <div class="col-10">
          <div class="container">
            <div class="row">
              <div class="card col-4" style="width:18rem  height:20px;" v-for="movie in movies" :key="movie.id">
                <img 
                  :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" 
                  class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ movie.title }}</h5>
                  <p class="card-text text-overflow: ellipsis" >{{ movie.overview }}</p>
                  <button class="btn btn-primary" @click="moveMovieDetail(movie)">Detail</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from'axios'

export default {
  name: 'Movie',
  data () {
    return {
      movies: null,
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

    getMovies() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/',
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.movies = res.data
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
        }})
    },

    // 정렬 함수 ---------------------------------------
    actionFilter () {
      const myPromise = new Promise((resolve, reject) => {
        axios({
          method: 'get',
          url: 'http://127.0.0.1:8000/movies/',
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            resolve()
            this.movies = res.data
          })
          .catch((err) => {
            console.log(err)
            reject()
          })
      })
      myPromise.then(() => {
        const newMovies = []
        this.movies.forEach((movie)=>{
          const genres = movie.genres
          for (const genre of genres) {
            if (genre === 28) {
              newMovies.push(movie)
            }
          }
        })
        if (newMovies) {
          this.movies = newMovies
        }
      })
    },


  },
  created: function () {
    if (localStorage.getItem('jwt')) {
      this.getMovies()
    } else {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>
