<template>
  <div style="font-family: 'Jua', sans-serif;">
    <h1>Community</h1>
    <hr>
    <div class="container">
      <p style="text-align:right;">
        <router-link :class="{ 'article-item': true }" style="text-decoration: none; color:gainsboro; text-align:right;" :to="{ name: 'CreateArticle' }">CreateArticle</router-link>
      </p>
      <div class="row">
        <div class="col-12">
          <div v-for="(article, index) in articles" :key="article.pk" class="fs-3">
            <p class="my-0 bg-dark text-white" style="text-align:left;">
              {{ index+1 }}. {{ article.title }}
              <router-link class="changelink fs-4"
                           style="color: darkred; text-decoration: none;"                            
                           :to="{ name: 'ArticleDetail', params: { article_id: article.id } }">Detail</router-link></p>
            <p class="my-0 form-control bg-dark" style="text-overflow: ellipsis; text-align:justify; height: 10rem;  color:gainsboro;">{{ article.content }}</p>
            <p class="my-0 bg-dark fs-5" style="text-align:right; color:gainsboro;">작성자 :{{ article.username }}</p>
            <p class="my-0 bg-dark fs-5" style="text-align:right; color:gainsboro;">작성 :{{ $moment(article.created_at).format('YYYY-MM-DD') }}</p>
            <p class="my-0 bg-dark fs-5" style="text-align:right; color:gainsboro;">수정 :{{ $moment(article.updated_at).format('YYYY-MM-DD') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'


export default {
  name: 'Article',

  data: function () {
    return {
      articles: null,
      userId: null,

      pageCnt: 0,
      pageNum: 0, 
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
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getArticles: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/articles/',
        headers: this.setToken()
      })
        .then((res) => {
          // console.log(res)
          this.articles = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },

  created: function () {
    if (localStorage.getItem('jwt')) {
      this.getUserId()
      this.getArticles()
    } else {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>

<style scoped>
.article-btn {
  margin-left: 10px;
}
.article-item {
  cursor: pointer;
  font-size: 1.5rem;
}
.article-item:hover {
  border: 2px solid dodgerblue;
}

</style>
