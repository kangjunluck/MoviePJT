<template>
  <div class="home">
    <h1>Movie</h1>
    <multiselect
      v-model="searchInput"
      :options="moviesTitleList"
      placeholder="영화제목을 입력해주세요"
      @searchChange="findMovie(searchInput)">
    </multiselect>
    <div class='container'>
      <div class="btn btn-primary" @click.prevent="getMovies">전체영화조회</div>
      <div class="row">
        <div class="col-2">
          <div class="w-100 btn-group btn-group-sm btn-group-vertical" role="group">
            <button class="btn b-panel" style="background-color: rgba(255, 255, 255, 0.1);" type="button" data-toggle="collapse" data-target="#collapseExample" aria-controls="collapseExample">
              장르 필터 
            </button>
            <div class="collapse mt-2 " id="collapseExample">     
              <div class="btn btn-primary" @click.prevent="genreFilter(28)">액션</div>
              <div class="btn btn-primary" @click.prevent="genreFilter(12)">모험</div>
              <label class="btn col text-left" style="background-color: rgba(255, 255, 255, 0.1);">
                <input type="checkbox" name="list_genre" value="액션"><label>액션</label>
              </label> 
            </div>        
          </div>
          <div class="btn btn-primary" @click.prevent="genreFilter(28)">액션</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(12)">모험</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(35)">코미디</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(80)">범죄</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(99)">다큐멘터리</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(10751)">가족</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(14)">판타지</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(36)">역사</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(27)">공포</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(10402)">음악</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(9648)">미스터리</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(10749)">로맨스</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(878)">SF</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(10700)">TV 영화</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(53)">스릴러</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(10752)">전쟁</div>
          <div class="btn btn-primary" @click.prevent="genreFilter(37)">서부</div>          
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
import Multiselect from 'vue-multiselect'

export default {
  name: 'Movie',
  components: { Multiselect },
  data () {
    return {
      movies: [],
      moviesTitleList: [],
      searchInput: null,
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
          var list = []
          this.movies.forEach(movie => {
            list.push(movie.title)
          });
          this.moviesTitleList = list
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
    findMovie (searchInput) {
      console.log(searchInput)
    },

    // 정렬 함수 ---------------------------------------
    genreFilter (genreId) {
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
            if (genre === genreId) {
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
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>