import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vSelect from 'vue-select'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons'
import {faFacebook, faLine, faLinkedin, faReddit, faTelegram, faTwitter} from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Vuelidate from 'vuelidate'
import SocialSharing from 'vue-social-sharing'


library.add(faQuestionCircle, faFacebook, faLine, faLinkedin, faReddit, faTelegram, faTwitter)

Vue.use(BootstrapVue)
Vue.use(SocialSharing);
Vue.component('v-select', vSelect)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
