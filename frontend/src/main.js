import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import store from './store'
import router from './router'
import './plugins/element.js'
import axios from 'axios'
import * as echarts from "echarts";
Vue.prototype.$echarts = echarts

Vue.config.productionTip = false
axios.defaults.withCredentials = true
new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')