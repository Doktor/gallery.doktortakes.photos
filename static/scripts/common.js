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

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const hexadecimal = "0123456789abcdef";

function getRandomHexString(length) {
  let arr = [];

  for (let i = 0; i < length; i++) {
    arr.push(hexadecimal.charAt(getRandomInt(0, hexadecimal.length)));
  }

  return arr.join('');
}

function queryString(params, skipBlank = false) {
  let escape = encodeURIComponent;

  let query = Object.entries(params).map(([key, value]) => {
    if (Array.isArray(value)) {
      return value.map(item => escape(key) + '=' + escape(item)).join('&');
    } else {
      if (skipBlank && value === '') { return; }
      return escape(key) + '=' + escape(value);
    }
  }).join('&');

  return '?' + query;
}

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

function isNumber(n) {
  return n.match(/^[0-9]+$/) !== null;
}

function getPageNumber() {
  let match = window.location.hash.match(/#page-([1-9][0-9]*)/);
  return (match === null) ? 1 : parseInt(match[1]);
}

function parseForm(el) {
  let data = new FormData(el);
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
      if (['tags', 'access', 'users', 'groups'].includes(key)) {
        params[key] = value ? value.split(',') : [];
      } else if (key === 'end') {
        params[key] = value ? value : null;
      } else {
        params[key] = value;
      }
    }
  }

  return params;
}

function sendRequest(method, url, onSuccess, onError,
                     data = null, useCSRF = false) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (request.readyState !== 4) {
      return;
    }

    let response;

    try {
      response = JSON.parse(request.responseText);
    } catch (e) {
      response = "Invalid server response: " + request.status.toString();
      return flash(response);
    }

    if (request.status !== 200) {
      onError(response);
    } else {
      onSuccess(response);
    }
  };

  request.open(method, url, true);

  if (useCSRF) {
    request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
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

function removeFlash(el) {
  el.classList.remove('visible');
  setTimeout(() => el.parentNode.removeChild(el), 200);
}

document.addEventListener('DOMContentLoaded', () => {
  Array.from(document.getElementsByClassName('message')).forEach((el) => {
    el.addEventListener('click', () => removeFlash(el));

    if (el.classList.contains('fade')) {
      setTimeout(() => removeFlash(el), 4000);
    }
  });
});

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

  el.addEventListener('click', () => removeFlash(el));

  messages.appendChild(el);

  setTimeout(() => el.classList.add('visible'), 100);
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
    containerEl, itemsPerPage, paginationSelector,
    {pages = 0, page = 0, saveHistory = true, loadRequired = false}) {
  this.containerEl = containerEl;
  this.itemsPerPage = itemsPerPage;
  this.paginationSelector = paginationSelector;
  this.pages = pages;
  this.page = page;
  this.saveHistory = saveHistory;
  this.loadRequired = loadRequired;

  if (this.loadRequired) {
    this.loadNewItems = function() {};
  } else {
    this.items = this.containerEl.children;
    this.validItems = this.items;
  }

  this.addButtons(this.pages);
  this.changePage(this.page, true);
};

Pagination.prototype.addDotsButton = function(container) {
  let el = document.createElement('span');
  el.innerText = '...';
  el.classList.add('page');

  el.addEventListener('click', (event) => {
    let dots = event.target;

    let input = document.createElement('input');
    input.classList.add('page-skip');

    input.addEventListener('blur', () =>{
      input.parentElement.replaceChild(dots, input);
    });

    input.addEventListener('keyup', (event) => {
      if (event.keyCode !== KEY_ENTER || !isNumber(input.value)) {
        return;
      }

      let page = parseInt(input.value);

      if (page > 0 && page <= this.pages) {
        this.changePage(page);
      }
    });

    dots.parentElement.replaceChild(input, dots);
    input.focus();
  });

  container.appendChild(el);
};

Pagination.prototype.addPageButton = function(page, container) {
  let el = document.createElement('span');
  el.classList.add('page');
  el.innerText = page.toString();
  el.dataset.page = page.toString();
  el.addEventListener('click', () => this.changePage(page));

  container.appendChild(el);
};

Pagination.prototype.createTextButton = function(text) {
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
        this.changePage(current - 1);
        break;
      case 'next':
        if (current === pages) { return; }
        this.changePage(current + 1);
        break;
    }
  });

  return el;
};

Pagination.prototype.addButtons = function() {
  let containers = document.querySelectorAll(this.paginationSelector);

  // Show/hide pagination containers
  for (let c of containers) {
    c.classList.toggle('hidden', this.pages <= 1);
  }

  if (this.pages <= 1) { return; }

  let current = this.page;
  let last = this.pages;

  for (let c of containers) {
    c.innerHTML = '';

    if (last >= 10) {
      this.addPageButton(1, c);

      // 1 ... 3 4 [5] 6 7 ... 20
      // 1 ... 14 15 [16] 17 18 ... 20
      if (current >= 5 && current <= last - 4) {
        this.addDotsButton(c);

        for (let page = current - 2; page <= current + 2; page++) {
          this.addPageButton(page, c);
        }

        this.addDotsButton(c);
      }

      // 1 ... 15 16 [17] 18 19 20
      // 1 ... 16 17 [18] 19 20
      else if (current > last - 4) {
        this.addDotsButton(c);

        for (let page = current - 2; page < last; page++) {
          this.addPageButton(page, c);
        }
      }

      // 1 2 [3] 4 5 ... 20
      // 1 2 3 [4] 5 6 ... 20
      else if (current <= 4) {
        for (let page = 2; page <= current + 2; page++) {
          this.addPageButton(page, c);
        }

        this.addDotsButton(c);
      }

      this.addPageButton(last, c);
    }

    else {
      for (let page = 1; page <= last; page++) {
        this.addPageButton(page, c);
      }
    }

    // Previous and next buttons
    if (last >= 2) {
      let prev = this.createTextButton('Prev');
      c.insertBefore(prev, c.firstChild);

      let next = this.createTextButton('Next');
      c.appendChild(next);
    }
  }
};

// Pagination: implementation

Pagination.prototype.changePage = function(page, force = false) {
  if (page === this.page && !force) { return; }

  this.page = page;

  if (this.loadRequired) {
    this.loadNewItems(() => {
      this.addButtons();
      this.selectPage();
    });
  } else {
    this.showLoadedItems();
    this.addButtons();
    this.selectPage();
  }
};

Pagination.prototype.selectPage = function() {
  // Deselect the previous selected page
  let selected = document.querySelectorAll('.page.selected');
  for (let item of selected) {
    item.classList.remove('selected');
  }

  // Select the new selected page
  let pageButtons = document.querySelectorAll(".page[data-page='{0}']".format(this.page));
  for (let item of pageButtons) {
    item.classList.add('selected');
  }

  if (this.saveHistory) {
    let url = document.location.search + '#page-' + this.page;
    history.replaceState(undefined, undefined, url);
  }
};

function loadItem(item) {
  let image = item.querySelector('img');

  if (image.classList.contains('not-loaded')) {
    image.src = image.dataset.src;
    image.classList.remove('not-loaded');
  }
}

Pagination.prototype.showLoadedItems = function() {
  if (this.page === 0) {
    for (let item of this.items) {
      item.classList.add('hidden');
    }

    return;
  }

  let start = this.itemsPerPage * (this.page - 1);
  let end = start + this.itemsPerPage - 1;

  Array.from(this.validItems).forEach((item, i) => {
    if (i >= start && i <= end) {
      loadItem(item);
      item.classList.remove('hidden');
    } else {
      item.classList.add('hidden');
    }
  });
};

Pagination.prototype.setValidItems = function(newItems) {
  this.validItems = newItems;
  this.pages = Math.ceil(newItems.length / this.itemsPerPage);
  this.changePage(this.pages === 0 ? 0 : 1, true);
};


// Search

const SEARCH_DELAY = 200;

let Search = function(pagination, items,
                      countEl, searchEl, noResultsEl) {
  this.pagination = pagination;
  this.items = items;
  this.countEl = countEl;
  this.searchEl = searchEl;
  this.noResultsEl = noResultsEl;

  this.previous = "";
  this.timeout = 0;

  this.searchEl.addEventListener('keyup', () => {
    if (this.searchEl.value === this.previous) { return; }
    this.previous = this.searchEl.value;

    // Starts filtering after a short delay
    clearTimeout(this.timeout);
    this.timeout = setTimeout(() => {
      this.matches = [];

      let term = this.searchEl.value.toLowerCase();

      for (let item of this.items) {
        if (item.dataset.name.includes(term)) {
          item.classList.remove('hidden');
          this.matches.push(item);
        } else {
          item.classList.add('hidden');
        }
      }

      this.pagination.setValidItems(this.matches);

      let n = this.matches.length;
      this.countEl.innerText = "{0} {1}".format(n, n === 1 ? 'album' : 'albums');
      this.noResultsEl.classList.toggle('hidden', n !== 0)
    }, SEARCH_DELAY);
  });
};
