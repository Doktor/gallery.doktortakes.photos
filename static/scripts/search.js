let $ = document.getElementById.bind(document);

const form = $('search');
const submit = $('submit');

const countEl = document.querySelector('#count');
const photos = document.querySelector('.photos');

const api = $('api');
const API_SEARCH = api.dataset.apiSearch;
const ITEMS_PER_PAGE = api.dataset.itemsPerPage;

// Update results

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

// Populates the search form from a query string
function populate_form(query) {
  query = query.substring(1, query.length);

  let items = query.split('&');

  for (let item of items) {
    let pair = item.split('=');
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

function get_search_query_string(page) {
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

  let query = query_string(params);

  let url = query + '#page-' + page;
  history.replaceState(undefined, undefined, url);

  params['page'] = page;
  query = query_string(params);

  return query;
}

document.addEventListener('DOMContentLoaded', function() {
  const pagination = new Pagination(photos, ITEMS_PER_PAGE, '.pagination', {load_required: true});

  function update_results(callback, query = '') {
    let url = API_SEARCH + (query || get_search_query_string(pagination.page));

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

      // Results
      for (let photo of response.photos) {
        let el = create_photo(photo);
        fragment.appendChild(el);
      }

      // Fill empty slots
      for (let i = response.photos.length; i < ITEMS_PER_PAGE; i++) {
        let el = create_empty_wrapper();
        fragment.appendChild(el);
      }

      photos.innerHTML = '';
      photos.appendChild(fragment);

      countEl.innerText = response.count;

      pagination.pages = Math.ceil(response.count / ITEMS_PER_PAGE);

      callback();
    };

    request.open('GET', url, true);
    request.send();
  }

  pagination.load_new_items = update_results;

  submit.addEventListener('click', () => { pagination.change_page(1); console.log(2); });

  if (window.location.search !== '') {
    populate_form(window.location.search);

    let page = get_page_number();
    pagination.change_page(page);
  } else {
    pagination.change_page(1);
  }
});
