// Additional prototype functions

Element.prototype.clearChildren = function() {
  while (this.firstChild) {
    this.removeChild(this.firstChild);
  }
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

// Utility functions

function query_string(params) {
  let escape = encodeURIComponent;
  let query = Object.keys(params)
    .map(function(key) {
      if (Array.isArray(params[key])) {
        return params[key].map(
          item => escape(key) + '=' + escape(item)).join('&');
      } else {
        return escape(key) + '=' + escape(params[key])
      }
    }).join('&');

  return '?' + query;
}

function get_cookie(name) {
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

function get_page_number() {
  let match = window.location.hash.match(/#page-(\d)/);
  return (match === null) ? 1 : parseInt(match[1])
}

// Key codes

const KEY_ENTER = 13;

const KEY_LEFT = 37;
const KEY_UP = 38;
const KEY_RIGHT = 39;
const KEY_DOWN = 40;

const KEY_A = 65;
const KEY_D = 68;
const KEY_H = 72;
const KEY_L = 76;

// Pagination: elements

let Pagination = function(items_per_page, pages, page) {
  this.items_per_page = items_per_page;
  this.pages = pages;
  this.page = page;

  this.load_required = false;
  this.load_new_items = function() {};
};

Pagination.prototype.setup = function() {
  this.add_buttons(this.pages);
  this.change_page(this.page, force = true);
};

Pagination.prototype.add_dots_button = function(container) {
  let el = document.createElement('span');
  el.innerText = '...';
  el.classList.add('page');

  el.addEventListener('click', function(event) {
    let dots = event.target;

    let input = document.createElement('input');
    input.classList.add('skip');

    input.addEventListener('blur', () =>{
      input.parentElement.replaceChild(dots, input);
    });

    input.addEventListener('keyup', (event) => {
      if (event.keyCode === KEY_ENTER && is_number(input.value)) {
        this.change_page(parseInt(input.value));
      }
    });

    dots.parentElement.replaceChild(input, dots);
    input.focus();
  });

  container.appendChild(el);
};

Pagination.prototype.add_page_button = function(page, container) {
  let el = document.createElement('span');
  el.classList.add('page');
  el.innerText = page.toString();
  el.dataset.page = page.toString();

  el.addEventListener('click', () => { this.change_page(page); });

  container.appendChild(el);
};

Pagination.prototype.create_text_button = function(text) {
  let el = document.createElement('span');
  el.innerText = text;
  el.classList.add('page');
  el.dataset.page = text.toLowerCase();

  el.addEventListener('click', () => {
    let current = this.page;
    let pages = this.pages;

    switch (el.dataset.page) {
      case 'prev':
        if (current === 1) { return; }
        this.change_page(current - 1);
        break;
      case 'next':
        if (current === pages) { return; }
        this.change_page(current + 1);
        break;
    }
  });

  return el;
};

Pagination.prototype.add_buttons = function() {
  let pagination = document.getElementsByClassName('pagination');

  // Show/hide pagination containers
  for (let container of pagination) {
    container.classList.toggle('hidden', this.pages <= 1);
  }

  if (this.pages <= 1) { return; }

  let current = this.page;
  let last = this.pages;

  for (let c of pagination) {
    c.innerHTML = '';

    if (last >= 10) {
      this.add_page_button(1, c);

      // 1 ... 3 4 [5] 6 7 ... 20
      // 1 ... 14 15 [16] 17 18 ... 20
      if (current >= 5 && current <= last - 4) {
        this.add_dots_button(c);

        for (let page = current - 2; page <= current + 2; page++) {
          this.add_page_button(page, c);
        }

        this.add_dots_button(c);
      }

      // 1 ... 15 16 [17] 18 19 20
      // 1 ... 16 17 [18] 19 20
      else if (current > last - 4) {
        this.add_dots_button(c);

        for (let page = current - 2; page < last; page++) {
          this.add_page_button(page, c);
        }
      }

      // 1 2 [3] 4 5 ... 20
      // 1 2 3 [4] 5 6 ... 20
      else if (current <= 4) {
        for (let page = 2; page <= current + 2; page++) {
          this.add_page_button(page, c);
        }

        this.add_dots_button(c);
      }

      this.add_page_button(last, c);
    }

    else {
      for (let page = 1; page <= last; page++) {
        this.add_page_button(page, c);
      }
    }

    // Previous and next buttons
    if (last >= 2) {
      let prev = this.create_text_button('Prev');
      c.insertBefore(prev, c.firstChild);

      let next = this.create_text_button('Next');
      c.appendChild(next);
    }
  }
};

// Pagination: implementation

Pagination.prototype.change_page = function(page, force = false) {
  if (page === this.page && !force) { return; }

  this.page = page;

  if (this.load_required) {
    this.load_new_items(() => {
      this.add_buttons();
      this.select_page();
    });
  } else {
    this.show_loaded_items();
    this.add_buttons();
    this.select_page();
  }
};

Pagination.prototype.select_page = function() {
  let selected = document.querySelectorAll('.page.selected');
  for (let item of selected) {
    item.classList.remove('selected');
  }

  let selector = ".page[data-page='{0}']".format(this.page);

  let pageButtons = document.querySelectorAll(selector);
  for (let item of pageButtons) {
    item.classList.add('selected');
  }

  if (!this.load_required) {
    let url = document.location.search + '#page-' + this.page;
    history.replaceState(undefined, undefined, url);
  }
};

Pagination.prototype.show_loaded_items = function() {
  let start = this.items_per_page * (this.page - 1);
  let end = start + this.items_per_page - 1;

  Array.from(photos.children).forEach((wrapper, i) => {
    let image = wrapper.querySelector('img');

    if (i >= start && i <= end) {
      if (!image.classList.contains('loaded')) {
        image.src = image.dataset.src;
        image.classList.remove('not-loaded');
        image.classList.add('loaded');
      }
      wrapper.classList.remove('hidden');
    } else {
      wrapper.classList.add('hidden');
    }
  });
};
