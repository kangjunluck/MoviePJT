<template>
  <div class="home">
    Home
    <div class="container">
      <div class="row">
        <div class="col-4">
          <h3>여기는 나닮배</h3>
        </div>
        <div class="col-4">
          <h3>오늘의 추천 영화</h3>
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

export default {
  name: 'Home',
  data () {
    return {
      userId: null,
      likeMovies: [],
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
  },
  created () {
    this.getUserId()
  },
}
</script>
