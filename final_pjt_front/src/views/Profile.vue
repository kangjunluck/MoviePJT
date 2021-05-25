<template>
  <div class="home">
    <h1>{{username}}의 Profile</h1>
    <hr>
    <h3>내가 쓴 article</h3>
    
    <p v-for="article in articles" :key="article.pk">
      <router-link :to="{ name: 'ArticleDetail', params: { article_id: article.id } }">{{ article.title }}</router-link>
    </p>
    <hr>
    <h3>내가 쓴 review</h3>
    <p v-for="review in reviews" :key="review.pk">
      <router-link :to="{ name: 'MovieDetail', params: { movie_id: review.movie_id } }">{{ review.content }}</router-link>
    </p>
    <hr>
    <h3>내가 쓴 comment</h3>
    <p v-for="comment in comments" :key="comment.pk">
      <router-link :to="{ name: 'ArticleDetail', params: { article_id: comment.article_id } }">{{ comment.content }}</router-link>
    </p>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'

export default {
  name: 'Profile',
  data: function () {
    return {      
      username: null,
      articles: null,
      comments: null,
      reviews: null,
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
  },
  created: function () {
    if (localStorage.getItem('jwt')) {
      this.getUserId() 
    } else {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>
