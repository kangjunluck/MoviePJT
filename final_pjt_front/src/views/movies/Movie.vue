<template>
  <div class="home" style="font-family: 'Jua', sans-serif;">
    <h1>Movie</h1>
    <div class='container'>
      <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
          <multiselect      
            v-model="searchInput"
            :options="moviesTitleList"
            placeholder="영화제목을 입력해주세요"
            @input="findMovie(searchInput)">
          </multiselect>
        </div>
      </div>
      <br>
      <hr>
      <div class="row">
        <div class="col-1">
          <div class="btn-group-vertical btn-group-toggle" data-toggle="buttons">        
            <label class="btn btn-primary my-1 border border-primary">
              <input type="radio" class="btn-check" name="options" autocomplete="off" @click="getMovies">전체 영화
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" autocomplete="off" @click.prevent="genreFilter(28)">액션
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option2" autocomplete="off" @click.prevent="genreFilter(12)">모험
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option3" autocomplete="off" @click.prevent="genreFilter(35)">코미디
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option4" autocomplete="off" @click.prevent="genreFilter(80)">범죄
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option5" autocomplete="off" @click.prevent="genreFilter(99)">다큐
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option6" autocomplete="off" @click.prevent="genreFilter(10751)">가족
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option7" autocomplete="off" @click.prevent="genreFilter(14)">판타지
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option8" autocomplete="off" @click.prevent="genreFilter(36)">역사
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option9" autocomplete="off" @click.prevent="genreFilter(27)">공포
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option10" autocomplete="off" @click.prevent="genreFilter(10402)">음악
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option11" autocomplete="off" @click.prevent="genreFilter(9648)">미스터리
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option12" autocomplete="off" @click.prevent="genreFilter(10749)">로맨스
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option13" autocomplete="off" @click.prevent="genreFilter(878)">SF
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option14" autocomplete="off" @click.prevent="genreFilter(10700)">TV 영화
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option15" autocomplete="off" @click.prevent="genreFilter(53)">스릴러
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option16" autocomplete="off" @click.prevent="genreFilter(10752)">전쟁
            </label>
            <label class="btn btn-outline-danger">
              <input type="radio" class="btn-check" name="options" id="option17" autocomplete="off" @click.prevent="genreFilter(37)">서부
            </label>
     
          </div>
        </div>
        <div class="col-11">
          <div class="container">
            <div class="row" id="my_movies">
              <content class="col-md-4 col-lg-4 col-sm-4" v-for="movie in itemsForList" :key="movie.id">
                <figure @mouseover="movieHover = true"
                        @mouseleave="movieHover = false"  class="myfigure">
                  <span style="font-size: 30px; text-align: center; background: black; color: white;">{{ movie.title }}</span>
                  <img @click="moveMovieDetail(movie)" :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path"  class="img-responsive img-rounded figure-img movie-img" valign="absmiddle" />                            
                  <div @click="moveMovieDetail(movie)" class="figure-overlay movie-img">                        
                    <div v-if="movieHover">   
                      <div class="figure-overlay-description">
                        <p style="font-size: 30px">{{movie.title}}</p>
                        개봉일:{{movie.release_date}} <br>
                        상영시간: {{movie.runtime}}분 <br>
                        평점: {{movie.vote_average}} <br>
                        user평점: {{movie.movie_vote}} <br>                                              
                      </div>       
                    </div>
                  </div>                  
                </figure>
              <hr>
              </content>
              <aside class="col-md-10 col-lg-10 col-sm-10">                 
              </aside>
              <b-pagination
                class="d-flex justify-content-center"
                v-model="currentPage"
                :total-rows="rows"
                :per-page="perPage"
                aria-controls="my-movies">
              </b-pagination>
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
      perPage : 9,
      currentPage : 1,    

      movieHover: false,
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
      myPromise.then(()=>{
        this.movies = this.movies.filter((movie)=>{
          return movie.title === searchInput
        })
      })
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
  },
  computed : {
    rows(){
        return this.movies.length;
    },
    itemsForList() {
      return this.movies.slice(
        (this.currentPage - 1) * this.perPage,
        this.currentPage * this.perPage,
      )
    },
  },
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.container content, .container aside {
  position: relative;
}

.myfigure {
  width: 100%;
  position: relative;
}

.figure-img {
  display: block;
  width: 100%;
  height: auto;
} 

.figure-overlay {
  position: absolute;
  top: 0;
  left: 0;
  overflow: auto;
  width: 100%;  
  color: #fff;
  margin: 0;
  display: block;  
  height: 100%;
    transform: scale(1);
  -webkit-transform: scale(1);
  -moz-transform: scale(1);
  -ms-transform: scale(1);
  -o-transform: scale(1);
  transition: all 0.5s ease-in-out;
  /* background: rgba(0, 0, 0, 0.6);
    -webkit-transition: .6s ease;
    transition: .6s ease;
  text-align: center; */

}

.figure-overlay-description {
  font-size: 15px;
  position: absolute;
  display: block;
  overflow: auto;
  top: 50%;
  left: 50%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  text-align: center;
}

.figure-overlay:hover {
  display: block;
  
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
    -webkit-transition: .6s ease;
    transition: .6s ease;
  text-align: center;
    transform: scale(1.1);
  -webkit-transform: scale(1.1);
  -moz-transform: scale(1.1);
  -ms-transform: scale(1.1);
  -o-transform: scale(1.1);
}

.movie-img {
  cursor: pointer;
}
.movie-img:hover {
  border: 5px solid crimson;
}
</style>