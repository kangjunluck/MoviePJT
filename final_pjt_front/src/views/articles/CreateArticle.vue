<template>
  <div style="font-family: 'Jua', sans-serif;">
    <h2>게시글 작성 중..</h2>
    <div class="container">
      <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
          <form>
            <p class="fs-3 my-0" style="text-align: left;">TITLE</p>
              <input type="text" class="form-control" style="background-color: gainsboro;" v-model.trim="title">
            <p class="fs-3 my-0" style="text-align: left;">CONTENT</p>
              <textarea class="form-control fs-4" style="background-color: gainsboro;" name="" id="" cols="30" rows="10" v-model.trim="content" ></textarea>
            <hr>
            <button class="fs-3" @click.prevent="createArticle">작성완료</button>
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
  name: 'CreateArticle',
  
  data: function () {
    return {
      title: null,
      content: null,
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
    createArticle: function () {
      const articleItem = {
        title: this.title,
        content: this.content,
      }

      if (articleItem.title && articleItem.content) {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/articles/',
          data: articleItem,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.$router.push({ name: 'Article' })
          })
          .catch((err) => {
            console.log(err)
          })
        }
    },
  },
}
</script>

<style>

</style>