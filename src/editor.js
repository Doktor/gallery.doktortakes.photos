import Vue from 'vue';
import VueRouter from 'vue-router';
import {router} from "./router/editor";
import {store} from "./store/editor";

import RouterEntryPoint from "./views/RouterEntryPoint.vue";


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
