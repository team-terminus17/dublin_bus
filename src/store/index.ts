import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    map: null,
    trackingStatus: false
  },
  mutations: {
    initMap(state, map) {
      state.map = map
    },

    changeTrackingStatus(state, status){
      state.trackingStatus = status;
    }
  }
})
