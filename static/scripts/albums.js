let $ = document.getElementById.bind(document);

const albumsEl = $('albums');
const countEl = document.querySelector('.count');
const searchEl = $('search');
const noResultsEl = $('no-results');

const SEARCH = $('search-api');
const COUNT = parseInt(SEARCH.dataset.count);
const ITEMS_PER_PAGE = parseInt(SEARCH.dataset.itemsPerPage);

// Search & pagination

document.addEventListener('DOMContentLoaded', function() {
  let page = getPageNumber();
  let pages = Math.ceil(COUNT / ITEMS_PER_PAGE);

  let pagination = new Pagination(
    albumsEl, ITEMS_PER_PAGE, '.pagination',
    {pages: pages, page: page, saveHistory: false});
  pagination.setup();

  let search = new Search(
    pagination, albumsEl, COUNT, countEl, searchEl, noResultsEl);
});
