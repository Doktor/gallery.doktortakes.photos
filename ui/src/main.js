import Vue from "vue";
import VueRouter from "vue-router";

import Base from "./pages/Base.vue";
import { router } from "./router/main.js";
import { store } from "./store";

import "./styles/main.scss";
import "./styles/forms.scss";

Vue.config.productionTip = process.env.NODE_ENV !== "production";
Vue.use(VueRouter);

(async function () {
  store.commit("setApiTokenFromLocalStorage");
  await store.dispatch("getUser");

  new Vue({
    el: "#app",

    router,
    store,

    components: {
      Base,
    },

    template: `<Base/>`,
  });
})();
