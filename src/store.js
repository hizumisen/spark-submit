import Vue from 'vue'
import Vuex from 'vuex'
import state from './state.json'

Vue.use(Vuex)

export default new Vuex.Store({
  state: state,
  mutations: {},
  actions: {}
})
