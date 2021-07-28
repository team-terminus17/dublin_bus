import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// I don't fully understand what is going on here. Is it enough
// to import these or do the other minified files in dist/js and dist/css
// need to be considered as well?
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";

import ownKeys = Reflect.ownKeys;
import Autocomplete from 'v-autocomplete'

Vue.use(Autocomplete)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
