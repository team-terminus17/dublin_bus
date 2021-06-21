import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

console.log("Hello from main.ts!")
fetch("/test").then(response => response.text()).then(data => console.log(data))

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
