let $ = document.getElementById.bind(document);

const api = $('api');
const photos = $('photos');

const COUNT = parseInt(api.dataset.count);
const ITEMS_PER_PAGE = parseInt(api.dataset.itemsPerPage);

const KEY_ENTER = 13;


function show_page(page) {
  let start = ITEMS_PER_PAGE * (page - 1);
  let end = start + ITEMS_PER_PAGE - 1;

  Array.from(photos.children).forEach(function(wrapper, i) {
    let imageEl = wrapper.querySelector('img');

    if (i >= start && i <= end) {
      if (!imageEl.classList.contains('loaded')) {
        imageEl.src = imageEl.dataset.src;
        imageEl.classList.remove('not-loaded');
        imageEl.classList.add('loaded');
      }
      wrapper.classList.remove('hidden');
    } else {
      wrapper.classList.add('hidden');
    }
  });

  let selected = document.querySelectorAll('.page.selected');
  for (let item of selected) {
    item.classList.remove('selected');
  }

  let pageButtons = document.querySelectorAll(".page[data-page='{0}']".format(page));
  for (let item of pageButtons) {
    item.classList.add('selected');
  }

  api.dataset.page = page;
  window.location.hash = 'page-' + page;
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

  container.appendChild(el);
}


function change_page(page) {
  if (page === api.dataset.page) {
    return;
  }

  show_page(page);
}


function click_page(event) {
  let el = event.target;
  change_page(el.dataset.page);
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
  if (last === 1) { return; }

  let pagination = document.getElementsByClassName('pagination');
  let results = COUNT !== 0;

  for (let container of pagination) {
    if (results) {
      container.classList.remove('hidden');
    } else {
      container.classList.add('hidden');
    }
  }

  if (!results) { return; }

  let current = parseInt(api.dataset.page);

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


function navigate_page(event) {
  let el = event.target;

  let current = parseInt(api.dataset.page);
  let pages = parseInt(api.dataset.pages);

  switch (el.dataset.page) {
    case 'prev':
      if (current === 1) { return; }
      return change_page(current - 1);
    case 'next':
      if (current === pages) { return; }
      return change_page(current + 1);
  }
}


document.addEventListener('DOMContentLoaded', function() {
  if (COUNT === 0) { return; }

  let match = window.location.hash.match(/#page-(\d)/);

  let current = match === null ? 1 : match[1];
  api.dataset.page = current;

  let count = Math.ceil(COUNT / ITEMS_PER_PAGE);
  api.dataset.pages = count;
  add_pages(count);

  show_page(current);
});


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
