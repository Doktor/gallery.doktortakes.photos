import Vue from 'vue';
import VueRouter from 'vue-router';

import RouterEntryPoint from "./views/RouterEntryPoint.vue";
import {router} from "./router/main.js";
import {store} from "./store/index.js";


Vue.config.productionTip = process.env.NODE_ENV !== 'production';
Vue.use(VueRouter);


const app = new Vue({
  el: '#app',

  router,
  store,

  components: {
    RouterEntryPoint,
  },

  created() {
    this.$store.dispatch('getUser');
  },

  template: `<RouterEntryPoint/>`,
});
