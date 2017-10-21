let $ = document.getElementById.bind(document);

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

Node.prototype.clearChildren = function() {
  while (this.firstChild) {
    this.removeChild(this.firstChild);
  }
};


// Update results

function parse_form() {
  let data = new FormData(form);
  let params = {};

  // Parse form data
  for (let pair of data.entries()) {
    let key = pair[0];
    let value = pair[1];

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

    photos.clearChildren();

    response.photos.forEach(function(photo) {
      let el = create_photo(photo);
      photos.appendChild(el);
    });

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
  image.src = p.thumbnail_url;

  link.appendChild(image);

  return wrapper;
}


// Pagination

function create_page_el(text, extra = null) {
  let el = document.createElement('span');
  el.innerText = text;
  el.classList.add('page');
  el.dataset.page = text.toLowerCase();

  if (extra !== null) {
    el.classList.add(extra);
  }

  return el;
}


function add_pages(pages) {
  let pagination = document.getElementsByClassName('pagination');
  let results = pages !== 0;

  for (let container of pagination) {
    if (results) {
      container.classList.remove('hidden');
    } else {
      container.classList.add('hidden');
    }
  }

  if (!results) { return; }

  let current = parseInt(pageEl.dataset.page);

  for (let container of pagination) {
    container.clearChildren();

    // Page number buttons
    for (let page = 1; page <= pages; page++) {
      let el = create_page_el(page.toString());

      if (current === page) {
        el.classList.add('selected');
      }

      el.addEventListener('click', change_page);

      container.appendChild(el);
    }

    // Previous and next buttons
    if (pages >= 2) {
      let prev = create_page_el('Prev', 'previous');
      prev.addEventListener('click', navigate_page);

      container.insertBefore(prev, container.firstChild);

      let next = create_page_el('Next', 'next');
      next.addEventListener('click', navigate_page);

      container.appendChild(next);
    }
  }
}


function navigate_page(event) {
  let el = event.target;

  let current = parseInt(pageEl.dataset.page);
  let pages = parseInt(pageEl.dataset.pages);

  switch (el.dataset.page) {
    case 'previous':
      if (current === 1) { return; }

      pageEl.dataset.page = current - 1;
      break;
    case 'next':
      if (current === pages) { return; }

      pageEl.dataset.page = current + 1;
      break;
  }

  update_results();
}


function change_page(event) {
  let el = event.target;

  if (el.dataset.page === pageEl.dataset.page) {
    return;
  }

  pageEl.dataset.page = el.dataset.page;

  update_results();
}


submit.addEventListener('click', update_results);

document.addEventListener('DOMContentLoaded', function() {
  update_results(API_SEARCH + window.location.search);
});
