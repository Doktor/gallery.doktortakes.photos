let $ = document.getElementById.bind(document);

Element.prototype.remove = function () {
  this.parentElement.removeChild(this);
};

function getCookie(name) {
  let value = null;

  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        value = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return value;
}

function query_string(params) {
  let escape = encodeURIComponent;
  let query = Object.keys(params)
    .map(key => escape(key) + '=' + escape(params[key]))
    .join('&');

  return '?' + query;
}

String.prototype.format = function() {
  "use strict";
  let str = this.toString();
  if (arguments.length) {
    let t = typeof arguments[0];
    let key;
    let args = ("string" === t || "number" === t) ?
        Array.prototype.slice.call(arguments) : arguments[0];

    for (key in args) {
      str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
    }
  }

  return str;
};

Node.prototype.clearChildren = function() {
  while (this.firstChild) {
    this.removeChild(this.firstChild);
  }
};

const flashContainer = $('flash');

const form = $('form');

const cover = $('cover');

const selected = [];
const photos = $('photos');

const totalCount = $('total-count');
const selectedCount = $('selected-count');

const api = $('api');

const API_ALBUM = api.dataset.apiAlbum;
const API_EDIT_LIST = api.dataset.apiEditList;
const API_DELETE_PHOTO = api.dataset.apiDeletePhoto;

const prefix = ' (';
const suffix = ')';


function flash(message) {
  for (let i = 0; i < flashContainer.children.length; i++) {
    let item = flashContainer.children[i];

    if (item.children[0].innerText === message) {
      let raw = item.children[1].innerText;
      let count = raw.substring(prefix.length, raw.length - 1);

      if (count === '') {
        count = 2;
      } else {
        count = parseInt(count) + 1;
      }

      item.children[1].innerText = prefix + count.toString() + suffix;
      return;
    }
  }

  let flashEl = document.createElement('div');
  flashEl.classList.add('flash');

  let text = document.createElement('span');
  text.innerText = message;
  flashEl.appendChild(text);

  let repeat = document.createElement('span');
  flashEl.appendChild(repeat);

  flashEl.addEventListener('click', function() {
    flashEl.classList.remove('visible');

    setTimeout(function() {
      flashEl.parentNode.removeChild(flashEl);
    }, 300);
  });

  flashContainer.appendChild(flashEl);

  setTimeout(function() {
    flashEl.classList.add('visible');
  }, 100);
}


function parse_form() {
  let data = new FormData(form);
  let params = {};

  // Parse form data
  for (let pair of data.entries()) {
    let key = pair[0], value = pair[1];

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

  return params;
}


function update_album() {
  let data = parse_form();

  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    let response = JSON.parse(request.responseText);

    if (request.status !== 200) {
      flash(response.error);
    } else {
      flash(response.message);

      api.dataset.albumPath = response.path;

      let name = response.name;

      let edit = $('album-edit-link');
      edit.href = response.edit_url;
      edit.innerText = name;

      $('album-name').innerText = name;
      $('album-link').href = response.url;

      window.history.replaceState('', response.title, response.edit_url);
    }
  };

  let params = { 'path': api.dataset.albumPath };
  let url = API_ALBUM + query_string(params);

  request.open("PUT", url, true);
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  request.send(JSON.stringify(data));
}

$('edit-album-submit').addEventListener('click', update_album);


function populate_edit_form() {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4 || request.status !== 200) {
      return;
    }

    let response = JSON.parse(request.responseText);

    for (let [key, value] of Object.entries(response)) {
      let selector = 'input[name="{0}"]'.format(key);

      let inputs = form.querySelectorAll(selector);
      let n = inputs.length;

      if (n === 1) {
        let el = inputs[0];
        el.value = value;
      }
    }
  };

  let params = { 'path': api.dataset.albumPath };
  let url = API_ALBUM + query_string(params);

  request.open("GET", url, true);
  request.send();
}


document.addEventListener('DOMContentLoaded', function() {
  populate_edit_form();
});


function change_cover() {
  if (selected.length !== 1) {
    return;
  }

  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    let response = JSON.parse(request.responseText);

    if (request.status !== 200) {
      flash(response.error);
    } else {
      flash(response.message);

      let fragment = document.createDocumentFragment();

      let a = document.createElement('a');
      a.href = response.cover.url;
      a.target = '_blank';
      a.title = 'Full size';

      let img = document.createElement('img');
      img.src = response.cover.thumbnail_url;

      a.appendChild(img);
      fragment.appendChild(a);

      cover.clearChildren();
      cover.appendChild(fragment);
    }
  };

  let params = { 'path': api.dataset.albumPath };
  let url = API_ALBUM + query_string(params);

  let data = {
    md5: selected[0].dataset.md5
  };

  request.open("PATCH", url, true);
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  request.send(JSON.stringify(data));
}


$('change-cover').addEventListener('click', change_cover);


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

      flash(response.message);
    } else {
      flash(response.error);
    }
  };

  let params = {
    'path': api.dataset.albumPath,
    'md5': wrapper.dataset.md5,
  };
  let url = API_DELETE_PHOTO + query_string(params);

  request.open("DELETE", url, true);
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
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
      flash(response.message);

      setTimeout(function() {
        window.location.href = API_EDIT_LIST;
      }, 3000);
    } else {
      flash(response.error);
    }
  };

  let params = {
    'name': $('delete-album-name').value,
    'path': api.dataset.albumPath,
  };
  let url = API_ALBUM + query_string(params);

  request.open("DELETE", url, true);
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
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

$('delete-album-submit').addEventListener('click', delete_album);
