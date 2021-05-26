<template>
  <div class="home">
    Similar
    {{ similarActor }}
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
