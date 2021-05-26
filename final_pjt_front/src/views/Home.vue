<template>
  <div class="home" style="font-family: 'Jua', sans-serif;">
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
            <figure @mouseover="movieHover = true"
                    @mouseleave="movieHover = false"  class="myfigure">
              <img @click="moveMovieDetail(ranMovie)" :src="'https://image.tmdb.org/t/p/w500/' + ranMovie.poster_path"  class="img-responsive img-rounded figure-img movie-img" valign="absmiddle" />                            
              <span style="font-size: 30px; text-align: center;  color: white;">{{ ranMovie.title }}</span>
              <div @click="moveMovieDetail(ranMovie)" class="figure-overlay movie-img">                        
                <div v-if="movieHover">   
                  <div class="figure-overlay-description">
                    <p style="font-size: 30px">{{ranMovie.title}}</p>
                    개봉일:{{ranMovie.release_date}} <br>
                    상영시간: {{ranMovie.runtime}}분 <br>
                    평점: {{ranMovie.vote_average}} <br>
                    user평점: {{ranMovie.movie_vote}} <br>                      
                  </div>       
                </div>
              </div>
            </figure>
          </div>
          <hr>
          <h2>최고 평점 영화 Top5</h2>        
          <div class="list-group">
            <div v-for="(rankmovie, index) in rankMovies" :key="rankmovie.id" :class="{'movie-img': true}">
              <button type="button" 
                      class="list-group-item list-group-item-action bg-dark border-0 d-flex justify-content-start" 
                      aria-current="true" data-bs-toggle="offcanvas" 
                      :data-bs-target="'#offcanvasBottom' + rankmovie.id" 
                      aria-controls="offcanvasBottom">
                <span class="fs-4" style="color: gainsboro">{{index+1}}위 - {{ rankmovie.title }} - {{ rankmovie.vote_average }}점</span>
              </button>
              <div class="offcanvas offcanvas-bottom text-dark" style="min-height: 25rem; background-color:gainsboro" tabindex="-1" :id="'offcanvasBottom' + rankmovie.id" aria-labelledby="offcanvasBottomLabel">
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
          <div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
            <div class="carousel-inner">
              <div class="carousel-item active" data-interval="2500">
                <img src="../assets/좋아요.png" class="d-block w-100" alt="...">
              </div>
              <div class="carousel-item" data-interval="2500" v-for="likemovie in likeMovies" :key="likemovie.id">
                <figure @mouseover="movieHover = true"
                        @mouseleave="movieHover = false"  class="myfigure">
                  <img @click="moveMovieDetail(likemovie)" :src="'https://image.tmdb.org/t/p/w500/' + likemovie.poster_path"  class="img-responsive img-rounded figure-img movie-img" valign="absmiddle" />
                  <div @click="moveMovieDetail(likemovie)" class="figure-overlay movie-img">                        
                    <div v-if="movieHover">   
                      <div class="figure-overlay-description">
                        <p style="font-size: 30px">{{likemovie.title}}</p>
                        개봉일:{{likemovie.release_date}} <br>
                        상영시간: {{likemovie.runtime}}분 <br>
                        평점: {{likemovie.vote_average}} <br>
                        user평점: {{likemovie.movie_vote}} <br>                      
                      </div>       
                    </div>
                  </div>
                </figure>
              </div>

            </div>
            <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="sr-only">Previous</span>
            </a>
            <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="sr-only">Next</span>
            </a>
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
      movieHover: false,
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
}

.movie-img {
  cursor: pointer;
  border: 2px solid transparent;
}
.movie-img:hover {
  border: 2px solid crimson;
}
</style>