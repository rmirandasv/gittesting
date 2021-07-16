import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Branch from '../views/Branch.vue'
import Commit from '../views/Commit.vue'
import PullRequest from '../views/PullRequest.vue'
import PullRequestList from '../views/PullRequestList'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/branch/:name',
    name: 'branch',
    component: Branch,
    props: true
  },
  {
    path: '/commits/:commitid',
    name: 'commit',
    component: Commit,
    props: true
  },
  {
    path: '/newpullrequest',
    name: 'newpullrequest',
    component: PullRequest
  },
  {
    path: '/pullrequest',
    name: 'pullrequests',
    component: PullRequestList
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
