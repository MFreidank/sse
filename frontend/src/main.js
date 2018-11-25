// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import App from './App'
import router from './router'
import Axios from 'axios'

Vue.use(Vuetify, {
  iconfont: 'mdi',
  theme: {
    primary: '#009688',
    secondary: '#FF5722',
    accent: '#FFAB91',
    error: '#F44336'
  }
})

Vue.prototype.$http = Axios

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
