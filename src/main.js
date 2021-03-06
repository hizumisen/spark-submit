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
import { faQuestionCircle, faCopy } from '@fortawesome/free-solid-svg-icons'
import {faFacebook, faLine, faLinkedin, faReddit, faTelegram, faTwitter} from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Vuelidate from 'vuelidate'
import SocialSharing from 'vue-social-sharing'
import VueClipboard from 'vue-clipboard2'
import VueCookieAcceptDecline from 'vue-cookie-accept-decline'
import 'vue-cookie-accept-decline/dist/vue-cookie-accept-decline.css'

library.add(faQuestionCircle, faCopy, faFacebook, faLine, faLinkedin, faReddit, faTelegram, faTwitter)

Vue.use(BootstrapVue)
Vue.use(SocialSharing);
Vue.use(VueClipboard)
Vue.component('v-select', vSelect)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('vue-cookie-accept-decline', VueCookieAcceptDecline)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
