let $ = document.getElementById.bind(document);

const KEY_ENTER = 13;

const form = $('search');
const submit = $('submit');

const countEl = $('count');
const photos = $('photos');

const pageEl = $('page');
const ITEMS_PER_PAGE = page.dataset.itemsPerPage;

const api = $('api');
const API_SEARCH = api.dataset.apiSearch;

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


// Update results

function parse_form() {
  let data = new FormData(form);
  let params = {};

  // Parse form data
  for (let pair of data.entries()) {
    let key = pair[0], value = pair[1];

    if (value === '') {
      continue;
    }

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

  params['page'] = pageEl.dataset.page;

  // Update browser history
  let base = document.location.href.replace(document.location.search, '');
  let query = query_string(params);

  window.history.pushState('', document.title, base + query);

  return query;
}


function update_results() {
  let query = parse_form();
  let url = API_SEARCH + query;

  // Create the request
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    if (request.status !== 200) {
      return console.log(request.responseText);
    }

    let response = JSON.parse(request.responseText);

    let fragment = document.createDocumentFragment();

    for (let i = 0; i < response.photos.length; i++) {
      let el = create_photo(response.photos[i]);
      fragment.appendChild(el);
    }

    for (let i = response.photos.length; i < ITEMS_PER_PAGE; i++) {
      let el = create_empty_wrapper();
      fragment.appendChild(el);
    }

    photos.innerHTML = '';
    photos.appendChild(fragment);

    countEl.innerText = response.count;

    let pages = Math.ceil(response.count / ITEMS_PER_PAGE);

    pageEl.dataset.pages = pages;
    add_pages(pages);
  };

  request.open('GET', url, true);
  request.send();
}

function create_photo(p) {
  let wrapper = document.createElement('div');
  wrapper.classList.add('wrapper');

  let photo = document.createElement('div');
  photo.classList.add('photo');

  wrapper.appendChild(photo);

  let link = document.createElement('a');
  link.href = p.url;

  photo.appendChild(link);

  let image = document.createElement('img');
  image.src = p.square_thumbnail_url;

  link.appendChild(image);

  return wrapper;
}

function create_empty_wrapper() {
  let el = document.createElement('div');
  el.classList.add('wrapper');
  el.classList.add('empty');

  return el;
}


// Pagination

function add_page_dots(container) {
  let el = document.createElement('span');
  el.innerText = '...';
  el.classList.add('page');

  el.addEventListener('click', function(event) {
    let dots = event.target;

    let input = document.createElement('input');
    input.classList.add('skip');

    input.addEventListener('blur', function() {
      input.parentElement.replaceChild(dots, input);
    });

    input.addEventListener('keyup', function(event) {
      if (event.keyCode === KEY_ENTER) {
        if (is_number(input.value)) {
          change_page(parseInt(input.value));
        }
      }
    });

    dots.parentElement.replaceChild(input, dots);
    input.focus();
  });

  container.appendChild(el);
}


function add_page_button(page, container) {
  let el = document.createElement('span');
  el.innerText = page.toString();
  el.classList.add('page');
  el.dataset.page = page.toString().toLowerCase();

  el.addEventListener('click', click_page);

  if (page === parseInt(pageEl.dataset.page)) {
    el.classList.add('selected');
  }

  container.appendChild(el);
}


function create_page_nav(text) {
  let el = document.createElement('span');
  el.innerText = text;
  el.classList.add('page');
  el.dataset.page = text.toLowerCase();

  el.addEventListener('click', navigate_page);

  return el;
}


function add_pages(last) {
  let pagination = document.getElementsByClassName('pagination');
  let results = last !== 0;

  for (let container of pagination) {
    if (results) {
      container.classList.remove('hidden');
    } else {
      container.classList.add('hidden');
    }
  }

  if (!results) { return; }

  let current = parseInt(pageEl.dataset.page);

  for (let c of pagination) {
    c.clearChildren();

    if (last >= 10) {
      add_page_button(1, c);

      // 1 ... 3 4 [5] 6 7 ... 20
      // 1 ... 14 15 [16] 17 18 ... 20
      if (current >= 5 && current <= last - 4) {
        add_page_dots(c);

        for (let page = current - 2; page <= current + 2; page++) {
          add_page_button(page, c);
        }

        add_page_dots(c);
      }

      // 1 ... 15 16 [17] 18 19 20
      // 1 ... 16 17 [18] 19 20
      else if (current > last - 4) {
        add_page_dots(c);

        for (let page = current - 2; page < last; page++) {
          add_page_button(page, c);
        }
      }

      // 1 2 [3] 4 5 ... 20
      // 1 2 3 [4] 5 6 ... 20
      else if (current <= 4) {
        for (let page = 2; page <= current + 2; page++) {
          add_page_button(page, c);
        }

        add_page_dots(c);
      }

      add_page_button(last, c);
    }

    else {
      for (let page = 1; page <= last; page++) {
        add_page_button(page, c);
      }
    }

    // Previous and next buttons
    if (last >= 2) {
      let prev = create_page_nav('Prev');
      c.insertBefore(prev, c.firstChild);

      let next = create_page_nav('Next');
      c.appendChild(next);
    }
  }
}


function change_page(page) {
  if (page === pageEl.dataset.page) {
    return;
  }

  pageEl.dataset.page = page;
  update_results();
}


function navigate_page(event) {
  let el = event.target;

  let current = parseInt(pageEl.dataset.page);
  let pages = parseInt(pageEl.dataset.pages);

  switch (el.dataset.page) {
    case 'previous':
      if (current === 1) { return; }
      return change_page(current - 1);
    case 'next':
      if (current === pages) { return; }
      return change_page(current + 1);
  }
}


function click_page(event) {
  let el = event.target;
  change_page(el.dataset.page);
}


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


function populate_form(query) {
  query = query.substring(1, query.length);

  let items = query.split('&');

  for (let pair of items) {
    pair = pair.split('=');
    let key = pair[0], value = pair[1];

    let selector = 'input[name="{0}"]'.format(key);

    let inputs = document.querySelectorAll(selector);
    let n = inputs.length;

    // Invalid name
    if (n === 0) { }

    else if (n === 1) {
      let el = inputs[0];

      if (el.type === 'checkbox' || el.type === 'radio') {
        // This can't happen with the default form
      } else {
        el.value = value;
      }
    }

    // Checkbox inputs only
    else {
      for (let el of inputs) {
        if (el.value === value) {
          el.checked = true;
          break;
        }
      }
    }
  }
}


submit.addEventListener('click', update_results);

document.addEventListener('DOMContentLoaded', function() {
  if (window.location.search !== '') {
    populate_form(window.location.search);
    update_results(API_SEARCH + window.location.search);
  }
});

document.addEventListener('DOMContentLoaded', function() {
  let fragment = document.createDocumentFragment();

  for (let i = 0; i < ITEMS_PER_PAGE; i++) {
    let el = create_empty_wrapper();
    fragment.appendChild(el);
  }

  photos.appendChild(fragment);
});
