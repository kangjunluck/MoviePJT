<template>
  <div class="profile" style="font-family: 'Jua', sans-serif;">
    <h1>{{ username }}의 Profile</h1>
    <hr>
    <div class='container'>
      <div class="row">
        <div class="col-4">
          <h3>작성한 Articles</h3>
          <div v-for="(article, index) in articles" :key="article.pk" class="fs-3">
            <p class="my-0 bg-dark text-white" style="text-align:left;">
              {{ index+1 }}. {{ article.title }}
              <router-link class="changelink fs-4"
                           style="color: darkred"                            
                           :to="{ name: 'ArticleDetail', params: { article_id: article.id } }">Detail</router-link></p>
            <p class="my-0 form-control" style="text-overflow: ellipsis; text-align:justify;">{{ article.content }}</p>
            <p class="my-0 bg-dark text-white fs-5" style="text-align:right;">작성 :{{ $moment(article.created_at).format('YYYY-MM-DD') }}</p>
            <p class="my-0 bg-dark text-white fs-5" style="text-align:right;">수정 :{{ $moment(article.updated_at).format('YYYY-MM-DD') }}</p>
          </div>
        </div>
        <div class="col-4">
          <h3>작성한 Reviews</h3>
          <div v-for="(review, index) in reviews" :key="review.pk" class="fs-3">
            <p class="my-0 bg-dark text-white" style="text-align:left;">
              {{ index+1 }}.
              <router-link class="changelink fs-4"
                           style="color: #E50914"                            
                           :to="{ name: 'MovieDetail', params: { movie_id: review.movie_id } }">Detail</router-link></p>
            <p class="my-0 form-control" style="text-overflow: ellipsis; text-align:justify;">{{ review.content }}</p>
          </div>


        </div>
        <div class="col-4">
          <h3>작성한 Comments</h3>
          <div v-for="(comment, index) in comments" :key="comment.pk" class="fs-3">
            <p class="my-0 bg-dark text-white" style="text-align:left;">
              {{ index+1 }}.
              <router-link class="changelink fs-4"
                           style="color: darkred"                            
                           :to="{ name: 'ArticleDetail', params: { article_id: comment.article_id } }">Detail</router-link></p>
            <p class="my-0 form-control" style="text-overflow: ellipsis; text-align:justify;">{{ comment.content }}</p>
            <p class="my-0 bg-dark text-white fs-5" style="text-align:right;">작성 :{{ $moment(comment.created_at).format('YYYY-MM-DD') }}</p>
            <p class="my-0 bg-dark text-white fs-5" style="text-align:right;">수정 :{{ $moment(comment.updated_at).format('YYYY-MM-DD') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'


export default {
  name: 'Profile',
  data: function () {
    return {      
      username: null,
      articles: null,
      comments: null,
      reviews: null,
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
          this.articles = res.data.articles
          this.reviews = res.data.reviews
          this.comments = res.data.comments
          this.username = res.data.username
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
<style scoped>
.changelink {
  text-decoration: none;
}
.move-over {
  cursor: pointer;
}
.move-over:hover {
  border: 5px solid crimson;
}
</style>