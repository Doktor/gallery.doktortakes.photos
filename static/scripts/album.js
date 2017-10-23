const about = document.getElementById('about');

const COUNT = about.dataset.count;
const ITEMS_PER_PAGE = about.dataset.itemsPerPage;

function showPage(page) {
  let start = ITEMS_PER_PAGE * (page - 1);
  let end = (ITEMS_PER_PAGE * page) - 1;

  let photos = document.getElementsByClassName('photo');
  for (let i = 0; i < photos.length; i++) {
    let photo = photos[i].children[0].children[0];
    let wrapper = photos[i].parentNode;

    if (i >= start && i <= end) {
      if (!photo.classList.contains('loaded')) {
        photo.src = photo.getAttribute('data-src');
        photo.classList.remove('loading');
        photo.classList.add('loaded');
      }
      wrapper.classList.remove('hidden');
    } else {
      wrapper.classList.add('hidden');
    }
  }
}

function showCurrentPage() {
  let page;
  let match = window.location.hash.match(/#page-(\d)/);
  if (match) {
    page = parseInt(match[1], 10);
  } else {
    page = 1;
  }

  showPage(page);
  $(function() {
    $('.pagination').pagination('selectPage', page);
  });
}

if (COUNT >= ITEMS_PER_PAGE) {
  $(function() {
    $('.pagination').pagination({
      items: COUNT,
      itemsOnPage: ITEMS_PER_PAGE,
      cssStyle: 'dark-theme',
      onInit: function() {
        showCurrentPage();
      },
      onPageClick: function(page, event) {
        showPage(page);
      }
    });
  });
} else {
  showCurrentPage();
}
