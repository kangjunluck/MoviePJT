<template>
  <div>
    <h2>수정 페이지</h2>
    <form>
      <p>title :<input type="text" v-model.trim="newtitle" ></p>
      <p>내용<br>
        <textarea name="" id="" cols="30" rows="10" v-model.trim="newcontent" ></textarea>
      </p>
      <button @click.prevent="updateClear">작성완료</button>
    </form>
  </div>
</template>

<script>
import axios from'axios'

export default {
  name: 'UpdateArticle',
  data () {
    return {
      id: this.$route.params.id,
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
                id: this.id,
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