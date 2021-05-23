<template>
  <div class="home">
    Profile
    <br>
    userpk: {{userId}}
    <br>
    user: {{userName}}
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'

export default {
  name: 'Profile',
  data: function () {
    return {      
      userId: null,
      userName: null,
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
          this.userName = res.data.username
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
