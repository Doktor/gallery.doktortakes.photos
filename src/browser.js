import Vue from 'vue';
import VueRouter from 'vue-router';

import RouterEntryPoint from "./views/RouterEntryPoint.vue";
import {router} from "./router/browser";
import {store} from "./store/editor";


Vue.config.productionTip = process.env.NODE_ENV !== 'production';
Vue.use(VueRouter);


const app = new Vue({
  el: '#app',

  router,
  store,

  components: {
    RouterEntryPoint,
  },

  template: `<RouterEntryPoint/>`,
});
