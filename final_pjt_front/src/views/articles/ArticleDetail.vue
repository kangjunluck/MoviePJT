<template>
  <div>
    <h2>Article Detail</h2>
    {{ newtitle }}<br>
    {{ newcontent }}
    <div v-if="newUserId === userId">
      <button @click="moveUpdate">수정</button>
      <button @click="deleteArticle">삭제</button>
    </div>
    <hr>
    <h2>Comment</h2>
    <ul>
      <li v-for="comment in comments" :key="comment.id">{{ comment.content }}<br>{{ comment.created_at }}<br>{{ comment.updated_at }}</li>
    </ul>
    <form>
      <p>내용 : <input type="text" v-model="comment_content"></p>      
      <button @click.prevent="commentCreate">+</button>
    </form>
  </div>
</template>

<script>
import axios from'axios'

export default {
  name: 'ArticleDetail',
  data () {
    return {
      id: this.$route.params.article_id,
      article: null,
      userId: '',
      newtitle: '',
      newcontent: '',
      newUserId: '',

      comments: null,
      comment_content: '',
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
          console.log('res')
          this.userId = res.data.userid
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getArticle() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/articles/${this.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.article = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },

    moveUpdate () {
      this.$router.push({
        name: 'UpdateArticle',
        params: {
          id: this.id,
        }
      })
    },
    deleteArticle: function () {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/articles/${this.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.$router.push({name: 'Article'})
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getComments() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/articles/${this.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.comments = res.data.comment_set
        })
        .catch((err) => {
          console.log(err)
        })
    },
    commentCreate () {
      const commentItem = {
        content: this.comment_content,
      }
      if (commentItem.content) {
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/articles/${this.id}/comment/`,
          data: commentItem,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.getComments()
          })
          .catch((err) => {
            console.log(err)
          })
        this.comment_content = ''
      }
    },
  },
  created () {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/articles/${this.id}/`,
      headers: this.setToken()
    })
      .then((response)=>{
        console.log(response)
        console.log('response')
        this.newtitle = response.data.title
        this.newcontent = response.data.content
        this.newUserId = response.data.userid
      })
      .catch((err)=>{
        console.log(err)
      })
    this.getUserId()
    this.getComments()
    this.getArticle()
  },
}
</script>

<style>

</style>