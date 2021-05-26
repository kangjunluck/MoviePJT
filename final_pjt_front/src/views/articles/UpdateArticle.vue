<template>
  <div style="font-family: 'Jua', sans-serif;">
    <h2>게시글 수정 중..</h2>
    <div class="container">
      <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
          <form>
            <p class="fs-3 my-0" style="text-align: left;">TITLE</p>
              <input type="text" class="form-control" style="background-color: gainsboro;" v-model.trim="newtitle">
            <p class="fs-3 my-0" style="text-align: left;">CONTENT</p>
              <textarea class="form-control fs-4" style="background-color: gainsboro;" name="" id="" cols="30" rows="10" v-model.trim="newcontent" ></textarea>
            <hr>
            <button class="fs-3" @click.prevent="updateClear">작성완료</button>
          </form>
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
  name: 'UpdateArticle',
  data () {
    return {
      id: this.$route.params.article_id,
      newtitle: '',
      newcontent: '',
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
    updateClear () {
      const articleItem = {
        title: this.newtitle,
        content: this.newcontent,
      }

      if (articleItem.title && articleItem.content) {
        axios({
          method: 'put',
          url: `http://127.0.0.1:8000/articles/${this.id}/`,
          data: articleItem,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.$router.push({
              name: 'ArticleDetail',
              params: {
                article_id: this.id,
              }
            })
          })
          .catch((err) => {
            console.log(err)
          })
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
        this.newtitle = response.data.title
        this.newcontent = response.data.content
      })
      .catch((err)=>{
        console.log(err)
      })
  }
}
</script>

<style>

</style>