let $ = document.getElementById.bind(document);

const api = $('api');
const photos = document.querySelector('.photos');

// Pagination

const COUNT = parseInt(api.dataset.count);
const ITEMS_PER_PAGE = parseInt(api.dataset.itemsPerPage);

document.addEventListener('DOMContentLoaded', function() {
  let page = get_page_number();
  let pages = Math.ceil(COUNT / ITEMS_PER_PAGE);

  const pagination = new Pagination(
    photos, ITEMS_PER_PAGE, {pages: pages, page: page, save_history: true});
  pagination.setup();
});

// Shortcuts

document.addEventListener('keydown', function(event) {
  let key = event.keyCode;

  switch (key) {
    case KEY_H:
      window.location.href = '/';
      break;
    case KEY_L:
      window.location.href = '/albums/';
      break;
  }
});
