let $ = document.getElementById.bind(document);

const form = $('album-form');

const cover = $('cover');

const selected = [];
const photos = document.querySelector('.photos');

const totalCount = $('total-count');
const selectedCount = $('selected-count');

const api = $('api');

const API_ALBUM = api.dataset.apiAlbum;
const API_PHOTO = api.dataset.apiPhoto;
const API_EDIT_LIST = api.dataset.apiEditList;


$('album-form-save').addEventListener('click', () => {
  let data = parse_form(form);

  function onError(response) {
    flash(response.error);
  }

  function onSuccess(response) {
    flash(response.message);

    api.dataset.albumPath = response.album.path;

    let name = response.album.name;

    let edit = $('album-edit-link');
    edit.href = response.edit_url;
    edit.innerText = name;

    $('album-name').innerText = name;
    $('album-link').href = response.album.url;

    window.history.replaceState('', response.title, response.edit_url);
  }

  send_request('PUT', API_ALBUM, onSuccess, onError, data, true);
});


$('set-parent').addEventListener('click', () => {
  $('album-set-parent-modal').classList.toggle('hidden');

  document.body.classList.toggle('modal-open');
});


$('album-set-parent-container').querySelectorAll('.wrapper').forEach((item) => {
  item.addEventListener('click', (event) => {
    event.preventDefault();

    $('f-parent').value = item.dataset.path;

    $('album-set-parent-modal').classList.toggle('hidden');
    document.body.classList.toggle('modal-open');

    flash("Parent album set.")
  })
});


document.addEventListener('DOMContentLoaded', () => {
  function onSuccess(response) {
    for (let [key, value] of Object.entries(response)) {
      let selector = '.field[name="{0}"]'.format(key);

      let inputs = form.querySelectorAll(selector);
      let n = inputs.length;

      if (n === 0) {
        // Do nothing
      } else if (n === 1) {
        let el = inputs[0];
        el.value = value;
      } else {
        // Input type: radio, checkbox
        selector = '{0}[value="{1}"]'.format(selector, value);
        let el = form.querySelector(selector);
        el.checked = true;
      }
    }
  }

  function onError() {}

  send_request('GET', API_ALBUM, onSuccess, onError);
});


$('change-cover').addEventListener('click', () => {
  if (selected.length !== 1) {
    return;
  }

  function onError(response) {
    flash(response.error);
  }

  function onSuccess(response) {
    flash(response.message);

    let fragment = document.createDocumentFragment();

    let a = document.createElement('a');
    a.href = response.album.cover.url;
    a.target = '_blank';
    a.title = 'Full size';

    let img = document.createElement('img');
    img.src = response.album.cover.thumbnail_url;

    a.appendChild(img);
    fragment.appendChild(a);

    cover.clearChildren();
    cover.appendChild(fragment);
  }

  let data = {md5: selected[0].dataset.md5};

  send_request('PATCH', API_ALBUM, onSuccess, onError, data, true);
});


function delete_photos() {
  selected.forEach((el) => delete_photo(el));
}

function delete_photo(el) {
  function onError(response) {
    flash(response.error);
  }

  function onSuccess(response) {
    el.remove();
    update_total();
    update_count();

    flash(response.message);
  }

  let params = {md5: el.dataset.md5};
  let url = API_PHOTO + query_string(params);

  send_request('DELETE', url, onSuccess, onError, null, true);
}

function delete_album() {
  function onError(response) {
    flash(response.error);
  }

  function onSuccess(response) {
    flash(response.message);

    setTimeout(function() {
      window.location.href = API_EDIT_LIST;
    }, 3000);
  }

  let params = {name: $('delete-album-name').value};
  let url = API_ALBUM + query_string(params);

  send_request('DELETE', url, onSuccess, onError, null, true);
}


function update_total() {
  totalCount.innerText = photos.children.length;
}

function update_count() {
  let selected = document.getElementsByClassName('selected');
  selectedCount.innerText = selected.length;
}

function select(el) {
  el.classList.add('selected');
  selected.push(el);

  update_count();
}

function deselect(el) {
  el.classList.remove('selected');

  let index = selected.indexOf(el);
  if (index !== -1) {
    selected.splice(index, 1);
  }

  update_count();
}

function invert(el) {
  !el.classList.contains('selected') ? select(el) : deselect(el);

  update_count();
}


document.addEventListener('DOMContentLoaded', function() {
  if (photos !== null) {
    for (let photo of photos.children) {
      photo.addEventListener('click', () => invert(photo));
    }

    $('select-all').addEventListener('click', function() {
      Array.from(photos.children).forEach(select);
    });

    $('select-none').addEventListener('click', function() {
      Array.from(photos.children).forEach(deselect);
    });

    $('select-invert').addEventListener('click', function() {
      Array.from(photos.children).forEach(invert);
    });
  }

  let subalbums = document.getElementsByClassName('children');

  for (let container of subalbums) {
    for (let photo of container.children) {
      photo.addEventListener('click', () => invert(photo));
    }
  }

  if (!(photos === null && subalbums.length === 0)) {
    $('delete-photos').addEventListener('click', delete_photos);
  }
});

$('album-delete-submit').addEventListener('click', delete_album);


// Search & pagination

const modal = $('album-set-parent-modal');

const albumsEl = modal.querySelector('#albums');
const countEl = modal.querySelector('.count');
const searchEl = modal.querySelector('#search');
const noResultsEl = modal.querySelector('#no-results');

const SEARCH = modal.querySelector('#search-api');
const COUNT = parseInt(SEARCH.dataset.count);
const ITEMS_PER_PAGE = parseInt(SEARCH.dataset.itemsPerPage);

document.addEventListener('DOMContentLoaded', function() {
  let pages = Math.ceil(COUNT / ITEMS_PER_PAGE);

  let pagination = new Pagination(albumsEl, ITEMS_PER_PAGE,
    {pages: pages, page: 1, save_history: false});
  pagination.setup();

  let search = new Search(pagination, albumsEl, COUNT,
    countEl, searchEl, noResultsEl);
});


Dropzone.autoDiscover = false;
const dropzone = new Dropzone("#dropzone", {
  paramName: 'files',
  parallelUploads: 3,
});
