const api = document.getElementById('api');
const photos = document.querySelector('.photos');

// Pagination

const COUNT = parseInt(api.dataset.count);
const ITEMS_PER_PAGE = parseInt(api.dataset.itemsPerPage);

document.addEventListener('DOMContentLoaded', function() {
  let page = getPageNumber();
  let pages = Math.ceil(COUNT / ITEMS_PER_PAGE);

  const pagination = new Pagination(
    photos, ITEMS_PER_PAGE, '.pagination',
    {pages: pages, page: page, saveHistory: true});
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
