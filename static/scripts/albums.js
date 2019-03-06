let $ = document.getElementById.bind(document);

const albumsEl = document.querySelector('.albums');
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

  const pagination = new Pagination(
    albumsEl, ITEMS_PER_PAGE, '.pagination',
    {pages: pages, page: page, saveHistory: false});

  const search = new Search(
    pagination, albumsEl.children, countEl, searchEl, noResultsEl);
});
