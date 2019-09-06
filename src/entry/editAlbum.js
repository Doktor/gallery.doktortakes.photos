import Vue from 'vue'
import EditAlbum from '../views/EditAlbum.vue'
import {store} from "../store/editAlbum/index.js";

Vue.config.productionTip = process.env.NODE_ENV !== 'production';

const app = new Vue({
  el: '#app',
  store,
  components: {
    EditAlbum,
  },
  template: `<EditAlbum/>`,
});
