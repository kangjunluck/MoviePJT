<template>
  <div>
    <h2>Article Detail</h2>
    {{ newtitle }}<br>
    {{ newcontent }}
    <button @click="moveUpdate">수정</button>
  </div>
</template>

<script>
import axios from'axios'

export default {
  name: 'ArticleDetail',
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
    moveUpdate () {
      this.$router.push({
        name: 'UpdateArticle',
        params: {
          id: this.id,
        }
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
        console.log('왓니?')
        this.newtitle = response.data.title
        this.newcontent = response.data.content
      })
      .catch((err)=>{
        console.log(err)
      })
  },
}
</script>

<style>

</style>