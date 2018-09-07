let $ = document.getElementById.bind(document);

const api = $('api');
const albums = $('albums');
const input = $('search');

const countEl = document.querySelector('.count');
const noResultsEl = $('no-results');

const SEARCH_DELAY = 200;
const COUNT = parseInt(api.dataset.count);
const ITEMS_PER_PAGE = parseInt(api.dataset.itemsPerPage);

let pagination;

// Search

function filter() {
  let term = input.value.toLowerCase();

  for (let item of document.getElementsByClassName('wrapper')) {
    let name = item.dataset.name;
    item.classList.toggle('hidden', !name.includes(term));
  }

  let hidden = document.querySelectorAll('#albums .hidden').length;
  let total = COUNT - hidden;
  let word = total === 1 ? 'album' : 'albums';

  pagination.update_page_count(total);
  countEl.innerText = "{0} {1}".format(total, word);
  noResultsEl.classList.toggle('hidden', total !== 0)
}

let timeout;

input.addEventListener('keyup', function() {
  if (input.value === input.dataset.previous) { return; }

  input.dataset.previous = input.value;

  clearTimeout(timeout);
  timeout = setTimeout(filter, SEARCH_DELAY);
});

// Pagination

document.addEventListener('DOMContentLoaded', function() {
  let page = get_page_number();
  let pages = Math.ceil(COUNT / ITEMS_PER_PAGE);

  pagination = new Pagination(albums, ITEMS_PER_PAGE, {pages: pages, page: page, save_history: false});
  pagination.setup();
});

// Shortcuts

document.addEventListener('keydown', function(event) {
  let key = event.keyCode;

  switch (key) {
    case KEY_H:
      window.location.href = '/';
      break;
  }
});
