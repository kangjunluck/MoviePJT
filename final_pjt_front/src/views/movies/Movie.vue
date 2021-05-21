<template>
  <div class="home">
    <h1>Movie</h1>
    <router-link :to="{ name: 'MovieDetail' }">두둥</router-link>

    <div class="container">
      <div class="row">
        <div class="card col-4" style="width: 18rem;" v-for="movie in movies" :key="movie.id">
          <img 
            :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" 
            class="card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.overview }}</p>
            <router-link :to="{ name: 'MovieDetail' }"><a href="#" class="btn btn-primary">Detail</a></router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src


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
