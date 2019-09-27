import Vue from 'vue'
import EditAlbums from '../views/EditAlbums.vue'
import {store} from "../store/editAlbums";

Vue.config.productionTip = process.env.NODE_ENV !== 'production';


const app = new Vue({
  el: '#app',
  store,
  components: {
    EditAlbums,
  },
  template: `<EditAlbums/>`,
});
