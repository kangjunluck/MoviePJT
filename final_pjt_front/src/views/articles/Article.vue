<template>
  <div>
    <h1>Article</h1>
    <router-link :to="{ name: 'CreateArticle' }">CreateArticle</router-link>
    <ul>
      <li v-for="(article, idx) in articles" :key="idx">
        <span @click="updateArticleStatus(article)" :class="{ completed: article.completed }">제목 : {{ article.title }}</span>
        <span  :class="{ completed: article.completed }">{{ article.content }}</span>
        <button @click="deleteArticle(article)" class="article-btn">X</button>
        <hr>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Article',
  data: function () {
    return {
      articles: null,
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

    getArticles: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/articles/',
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.articles = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
    deleteArticle: function (article) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/articles/${article.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.getArticles()
        })
        .catch((err) => {
          console.log(err)
        })
    },
    updateArticleStatus: function (article) {
      const articleItem = {
        ...article,
        completed: !article.completed
      }

      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/articles/${article.id}/`,
        data: articleItem,
        headers: this.setToken(),
      })
        .then((res) => {
          console.log(res)
          article.completed = !article.completed
        })
      },
    },
  // created: function () {
  //   if (localStorage.getItem('jwt')) {
  //     this.getArticles()
  //   } else {
  //     this.$router.push({name: 'Login'})
  //   }
  // }
}
</script>

<style scoped>
  .article-btn {
    margin-left: 10px;
  }

  .completed {
    text-decoration: line-through;
    color: rgb(112, 112, 112);
  }
</style>
