import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import axios from 'axios'

Vue.config.productionTip = false

axios.defaults.baseURL = 'http://localhost:8000/api'
axios.defaults.headers['Accept'] = 'application/json'
axios.defaults.headers['Content-Type'] = 'application/json'

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
