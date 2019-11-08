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

  template: `<RouterEntryPoint/>`,
});


// Utility functions

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

// Notifications

const messages = document.getElementById('messages');

function removeFlash(el) {
  el.classList.remove('visible');
  setTimeout(() => el.parentNode.removeChild(el), 200);
}

export function flash(message) {
  for (let i = 0; i < messages.children.length; i++) {
    let item = messages.children[i];

    if (item.children[0].innerText === message) {
      let raw = item.children[1].innerText;
      let count = raw.substring(2, raw.length - 1);

      if (count === '') {
        count = 2;
      } else {
        count = parseInt(count) + 1;
      }

      item.children[1].innerText = ' (' + count.toString() + ')';
      return;
    }
  }

  let el = document.createElement('div');
  el.classList.add('message');

  let text = document.createElement('span');
  text.innerText = message;
  el.appendChild(text);

  let repeat = document.createElement('span');
  el.appendChild(repeat);

  el.addEventListener('click', () => removeFlash(el));

  messages.appendChild(el);

  setTimeout(() => el.classList.add('visible'), 100);

  return el;
}
