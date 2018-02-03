Element.prototype.clearChildren = function() {
  while (this.firstChild) {
    this.removeChild(this.firstChild);
  }
};

Element.prototype.remove = function () {
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


function getCookie(name) {
  let value = null;

  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        value = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return value;
}

function is_number(n) {
  return n.match(/^[0-9]+$/) !== null;
}


// Key codes
const KEY_LEFT = 37;
const KEY_UP = 38;
const KEY_RIGHT = 39;
const KEY_DOWN = 40;

const KEY_A = 65;
const KEY_D = 68;
const KEY_H = 72;
const KEY_L = 76;
