import Vue from 'vue';
import VueRouter from 'vue-router';
import {mapActions} from 'vuex';

import Base from "./views/Base.vue";
import {router} from "./router/main.js";
import {store} from "./store/index.js";

import "./styles/common.scss";
import "./styles/main.scss";


Vue.config.productionTip = process.env.NODE_ENV !== 'production';
Vue.use(VueRouter);


const app = new Vue({
  el: '#app',

  router,
  store,

  components: {
    Base,
  },

  template: `<Base/>`,

  methods: {
    ...mapActions([
      'getUser',
    ]),
  },

  async created() {
    await this.getUser();
  },
});


// Utility functions

export function randomChoice(items) {
  let index = Math.floor(Math.random() * items.length);
  return items[index];
}

Array.prototype.clear = function() {
  this.splice(0, this.length);
};

Array.prototype.remove = function(item) {
  this.splice(this.indexOf(item), 1);
};

Element.prototype.remove = function() {
  this.parentElement.removeChild(this);
};

String.prototype.format = function() {
  "use strict";
  let str = this.toString();
  if (arguments.length) {
    let t = typeof arguments[0];
    let key;
    let args = ("string" === t || "number" === t) ?
        Array.prototype.slice.call(arguments) : arguments[0];

    for (key in args) {
      str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
    }
  }

  return str;
};
