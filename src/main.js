import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vSelect from 'vue-select'
import vCluster from './components/Cluster.vue'

Vue.use(BootstrapVue)
Vue.config.productionTip = false
Vue.component('v-select', vSelect)
Vue.component('v-cluster', vCluster)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
