let $ = document.getElementById.bind(document);

Element.prototype.remove = function () {
  this.parentElement.removeChild(this);
};

function query_string(params) {
  let escape = encodeURIComponent;
  let query = Object.keys(params)
    .map(key => escape(key) + '=' + escape(params[key]))
    .join('&');

  return '?' + query;
}

const selected = [];
const photos = $('photos');

const totalCount = $('total-count');
const selectedCount = $('selected-count');

const api = $('api');

const API_EDIT_LIST = api.dataset.apiEditList;
const API_DELETE_PHOTO = api.dataset.apiDeletePhoto;
const API_DELETE_ALBUM = api.dataset.apiDeleteAlbum;


function delete_photos() {
  for (let wrapper of selected) {
    delete_photo(wrapper);
  }
}

function delete_photo(wrapper) {
   let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4 || request.status !== 200) {
      return;
    }

    let response = JSON.parse(request.responseText);

    if (response.success) {
      wrapper.remove();
      update_total();
      update_count();
    }
  };

  let params = {
    'path': api.dataset.albumPath,
    'md5': wrapper.dataset.md5,
  };
  let url = API_DELETE_PHOTO + query_string(params);

  request.open("GET", url, true);
  request.send();
}

function delete_album() {
   let request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (request.readyState !== 4 || request.status !== 200) {
      return;
    }

    let response = JSON.parse(request.responseText);

    if (response.success) {
      window.location.href = API_EDIT_LIST;
    } else {
      alert(response.error);
    }
  };

  let params = {
    'name': $('delete-album-name').value,
    'path': api.dataset.albumPath,
  };
  let url = API_DELETE_ALBUM + query_string(params);

  request.open("GET", url, true);
  request.send();
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
}

function deselect(el) {
  el.classList.remove('selected');

  let index = selected.indexOf(el);
  if (index !== -1) {
    selected.splice(index, 1);
  }
}


document.addEventListener('DOMContentLoaded', function() {
  for (let photo of photos.children) {
    photo.addEventListener('click', function() {
      !this.classList.contains('selected') ? select(this) : deselect(this);
      update_count();
    });
  }
});

$('delete-photos').addEventListener('click', delete_photos);

$('select-all').addEventListener('click', function() {
  Array.from(photos.children).forEach(select);
  update_count();
});

$('select-none').addEventListener('click', function() {
  Array.from(photos.children).forEach(deselect);
  update_count();
});

$('delete-album-submit').addEventListener('click', delete_album);
