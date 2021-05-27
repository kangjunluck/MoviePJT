<template>
  <div style="font-family: 'Jua', sans-serif;">
    <h2>Title : {{ article.title }}</h2>
    <div class="container">
      <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
          <div class="fs-3">
            <p class="my-0 bg-dark text-white" style="text-align:left;">
              작성자 : {{ article.username }}</p>
            <p class="my-0 form-control bg-dark fs-3" style="overflow: auto; text-align:justify; height: 30rem;  color:gainsboro;">{{ article.content }}</p>
            <p class="my-0 bg-dark fs-5" style="text-align:right; color:gainsboro;">작성 :{{ $moment(article.created_at).format('YYYY-MM-DD') }}</p>
            <p class="my-0 bg-dark fs-5" style="text-align:right; color:gainsboro;">수정 :{{ $moment(article.updated_at).format('YYYY-MM-DD') }}</p>
          </div>
          <div v-if="newUserId === userId">
            <button @click="moveUpdate">수정</button>
            <button @click="deleteArticle">삭제</button>
          </div>
          <hr>
          <h4 style="text-align: left;">Comments</h4>

          <form>
            <span>댓글 작성 <input type="text" style="width: 30rem;" v-model="comment_content"></span>      
            <button @click.prevent="commentCreate">추가</button>
          </form>
          <div v-for="(comment,index) in comments" :key="comment.id" class="fs-3">
            <div v-if="comment.completed" class="fs-6">
              <div class="d-flex justify-content-between">
                <div class="fs-4">
                  {{ comment.comment_user }}의 댓글 수정중
                </div>
                <button class="fs-6" @click.prevent="updateComment(comment)">완료</button>
              </div>
              <input class="form-control" type="text" v-model="comment.content">
            </div>
            <div v-else>
              <div class="d-flex justify-content-between">
                <div class="my-0 bg-dark text-white fs-4" style="text-align:left;">
                  {{ index+1 }}. {{ comment.comment_user }}
                </div>
                <div v-if="comment.user === userId">
                  <button class="fs-6" @click.prevent="updateComment(comment)">수정</button>
                </div>
              </div>
              <p class="my-0 form-control bg-dark" style="text-overflow: ellipsis; text-align:justify;  color:gainsboro;">{{ comment.content }}</p>
              <p class="my-0 bg-dark fs-6" style="text-align:right; color:gainsboro;">작성 :{{ $moment(comment.created_at).format('YYYY-MM-DD') }}</p>
              <p class="my-0 bg-dark fs-6" style="text-align:right; color:gainsboro;">수정 :{{ $moment(comment.updated_at).format('YYYY-MM-DD') }}</p>
            </div>
            <div v-if="comment.user === userId" class="d-flex flex-row-reverse">
              <button class="fs-6" @click.prevent="deleteComment(comment)">삭제</button>
            </div>
          </div>
        </div>
        <div class="col-2">
        </div>
      </div>
    </div>
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
          article_id: this.id,
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

    updateComment(comment) {
      const commentItem = {
        ...comment,
        'content': comment.content,
        'completed': !comment.completed,
      }
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/articles/comment/${comment.id}/`,
        data: commentItem,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          comment.completed = !comment.completed
        })
        .catch((err) => {
          console.log(err)
        })

    },
    deleteComment(comment) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/articles/comment/${comment.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.getComments()
        })
        .catch((err) => {
          console.log(err)
        })
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