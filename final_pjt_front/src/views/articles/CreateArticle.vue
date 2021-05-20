<template>
  <div>
    <form>
      <p>title :<input type="text" v-model.trim="title" ></p>
      <p>내용<br>
        <textarea name="" id="" cols="30" rows="10" v-model.trim="content"></textarea>
      </p>
      <button @click.prevent="createArticle">작성완료</button>
    </form>
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