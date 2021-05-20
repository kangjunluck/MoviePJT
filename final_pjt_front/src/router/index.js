import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

import Article from '../views/articles/Article.vue'
import CreateArticle from '../views/articles/CreateArticle.vue'

import Movie from '../views/Movie.vue'
import Profile from '../views/Profile.vue'
import Similar from '../views/Similar.vue'

import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/movie',
    name: 'Movie',
    component: Movie
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/articles',
    name: 'Article',
    component: Article
  },
  {
    path: '/articles/create',
    name: 'CreateArticle',
    component: CreateArticle
  },
  {
    path: '/similar',
    name: 'Similar',
    component: Similar
  },

  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router