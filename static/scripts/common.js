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
  let match = window.location.hash.match(/#page-([1-9][0-9]*)/);
  return (match === null) ? 1 : parseInt(match[1]);
}

function parse_form(formEl) {
  let data = new FormData(formEl);
  let params = {};

  // Parse form data
  for (let pair of data.entries()) {
    let key = pair[0], value = pair[1];

    if (key in params) {
      if (Array.isArray(params[key])) {
        params[key].push(value);
      } else{
        params[key] = [params[key], value]
      }
    } else {
      params[key] = value;
    }
  }

  return params;
}

function send_request(method, url, onSuccess, onError,
                      data = null, useCSRF = false) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (request.readyState !== 4) {
      return;
    }

    let response = JSON.parse(request.responseText);

    if (request.status !== 200) {
      onError(response);
    } else {
      onSuccess(response);
    }
  };

  request.open(method, url, true);

  if (useCSRF) {
    request.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
  }

  if (data !== null) {
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
  } else {
    request.send();
  }
}


// Notifications

const messages = document.getElementById('messages');

function flash(message) {
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

  el.addEventListener('click', function() {
    el.classList.remove('visible');

    setTimeout(function() {
      el.parentNode.removeChild(el);
    }, 300);
  });

  messages.appendChild(el);

  setTimeout(function() {
    el.classList.add('visible');
  }, 100);
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

let Pagination = function(
    container_el, items_per_page, paginationSelector,
    {pages = 0, page = 0, save_history = true, load_required = false}) {
  this.containerEl = container_el;
  this.items_per_page = items_per_page;
  this.paginationSelector = paginationSelector;
  this.pages = pages;
  this.page = page;
  this.save_history = save_history;
  this.load_required = load_required;

  if (this.load_required) {
    this.load_new_items = function() {};
  }
};

Pagination.prototype.setup = function() {
  this.add_buttons(this.pages);
  this.change_page(this.page, true);
};

Pagination.prototype.add_dots_button = function(container) {
  let el = document.createElement('span');
  el.innerText = '...';
  el.classList.add('page');

  el.addEventListener('click', (event) => {
    let dots = event.target;

    let input = document.createElement('input');
    input.classList.add('skip');

    input.addEventListener('blur', () =>{
      input.parentElement.replaceChild(dots, input);
    });

    input.addEventListener('keyup', (event) => {
      if (event.keyCode !== KEY_ENTER || !is_number(input.value)) {
        return;
      }
      
      let page = parseInt(input.value);

      if (page > 0 && page <= this.pages) {
        this.change_page(page);
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

Pagination.prototype.update_page_count = function(count) {
  this.pages = Math.ceil(count / this.items_per_page);
  this.change_page(this.pages === 0 ? 0 : 1, true, true);
};

Pagination.prototype.add_buttons = function() {
  let pagination = document.querySelectorAll(this.paginationSelector);

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

Pagination.prototype.change_page = function(page, force = false, ignore_hidden = false) {
  if (page === this.page && !force) { return; }

  this.page = page;

  if (this.load_required) {
    this.load_new_items(() => {
      this.add_buttons();
      this.select_page();
    });
  } else {
    this.show_loaded_items(ignore_hidden);
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

  if (this.save_history) {
    let url = document.location.search + '#page-' + this.page;
    history.replaceState(undefined, undefined, url);
  }
};

Pagination.prototype.show_loaded_items = function(ignore_hidden = false) {
  if (this.page === 0) {
    for (let wrapper of this.containerEl.children) {
      wrapper.classList.add('hidden');
    }

    return;
  }

  let start = this.items_per_page * (this.page - 1);
  let end = start + this.items_per_page - 1;

  Array.from(this.containerEl.children).forEach((wrapper, i) => {
    if (ignore_hidden && wrapper.classList.contains('hidden')) { return; }

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


// Search

const SEARCH_DELAY = 200;

let Search = function(pagination, elements, count,
                      countEl, searchEl, noResultsEl) {
  this.pagination = pagination;
  this.elements = elements;
  this.count = count;
  this.countEl = countEl;
  this.searchEl = searchEl;
  this.noResultsEl = noResultsEl;

  let timeout;

  this.searchEl.addEventListener('keyup', () => {
    if (this.searchEl.value === this.searchEl.dataset.previous) { return; }

    this.searchEl.dataset.previous = this.searchEl.value;

    clearTimeout(timeout);
    timeout = setTimeout(() => {
      let term = this.searchEl.value.toLowerCase();

      for (let item of this.elements.querySelectorAll('.wrapper')) {
        let name = item.dataset.name;
        item.classList.toggle('hidden', !name.includes(term));
      }

      let hidden = this.elements.querySelectorAll('.hidden').length;
      let total = this.count - hidden;
      let word = total === 1 ? 'album' : 'albums';

      this.pagination.update_page_count(total);
      this.countEl.innerText = "{0} {1}".format(total, word);
      this.noResultsEl.classList.toggle('hidden', total !== 0)
    }, SEARCH_DELAY);
  });
};
