<template>
  <div class="home" style="font-family: 'Jua', sans-serif;">
    <h1>나닮배(나를 닮은 배우)</h1>
    <hr>
    <a class="fs-2" href="http://127.0.0.1:8000/movies/uploadimg/">사진등록하러가기</a><br><hr><br>    
    <div v-if="similarActor">
      <div class="container fs-3">
        <div class="row" style="height:30rem;">        
          <div class="col-md-5">
            <h1>등록한 사진??</h1>   
            <hr>
            <img style="height:25rem;" :src="'http://127.0.0.1:8000/media/' + imgName" alt="">                                            
          </div>
          <div class="col-md-2 d-flex flex-column justify-content-center aligns-content-center">         
            <a class="fs-1 noline" :href="googleUrl" target='_blank'>{{ similarActor.actor_name }}</a>   
            <p class="fs-2">{{ similarActor.actor_confidence.toFixed(4) * 100 }}%</p>
            <p>일치!!</p>
          </div>
          <div class="col-md-5">
            <h1>나(등록한 사진)를 닮은 배우는??</h1>   
            <hr>
            <img style="height:25rem;" :src="actorUrl" alt=""><br>                              
          </div>
        </div>
        <hr>
        <h1>나닮배가 나온 영화</h1>
        <div>
          <div v-for="(movie, index) in similarActor.movie_list" :key="index">
            {{ index+1 }}.
            <a class="fs-2 noline" :href="baseUrl + movie" target='_blank'> {{ movie }}</a>                           
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>사진을 먼저 등록해 주세요</p>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'

export default {
  name: 'Similar',
  data: function () {
    return {      
      username: null,
      articles: null,
      comments: null,
      reviews: null,
      similarActor: null,
      baseUrl: 'https://www.google.com/search?q=',
      googleUrl: '',
      imgName: null,
      actorUrl: null,
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
          this.articles = res.data.articles
          this.reviews = res.data.reviews
          this.comments = res.data.comments
          this.username = res.data.username
        })
        .catch((err) => {
          console.log(err)
        })
    },
    findActor () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/findactor/',
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.similarActor = res.data
          this.imgName = res.data.imgname
          this.googleUrl = this.baseUrl + res.data.actor_name
          this.actorUrl = res.data.actor_img_url
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },
  created: function () {
    if (localStorage.getItem('jwt')) {
      this.getUserId() 
      this.findActor()
    } else {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>
<style scoped>
.noline {
  text-decoration: none;
}
</style>