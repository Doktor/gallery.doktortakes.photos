import Vue from 'vue';
import Vuex from "vuex";
import NewAlbum from '../views/NewAlbum.vue';
import {store} from "../store/newAlbum";


Vue.config.productionTip = process.env.NODE_ENV !== 'production';
Vue.use(Vuex);

const app = new Vue({
  el: '#app',
  store,
  components: {
    NewAlbum,
  },
  template: `<NewAlbum/>`,
});
