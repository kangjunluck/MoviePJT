<template>
  <div>
    <h1>Login</h1>
    <div class="container">
      <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
          <div class="d-flex flex-column align-items-start">
            <label for="username">사용자 이름</label>
            <input type="text" id="username"  class="form-control" v-model="credentials.username">
            <small id="nameHelp">We'll never share your ID with anyone else.</small>
          </div>
          <div class="d-flex flex-column align-items-start">
            <label for="password">Password</label>
            <input type="password" id="password"  class="form-control" v-model="credentials.password">
          </div>
          <button @click="login" class="btn btn-primary my-2">Submit</button>
        </div>
        <div class="col-2">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

// const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      }
    }
  },
  methods: {
    login: function () {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/login/',
        data: this.credentials,
      })
        .then(res => {
          console.log(res)
          localStorage.setItem('jwt', res.data.token)
          this.$emit('login')
          this.$router.push({ name: 'Home' })
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
