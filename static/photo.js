// Arrow keys
const KEY_LEFT = 37;
const KEY_UP = 38;
const KEY_RIGHT = 39;
const KEY_DOWN = 40;

// API paths
const api = document.getElementById('api');

const API_PREVIOUS = api.dataset.urlPrevious;
const API_NEXT = api.dataset.urlNext;
const API_FIRST = api.dataset.urlFirst;
const API_LAST = api.dataset.urlLast;

// Shortcut key mapping
const KEY_MAPPING = {
  [KEY_LEFT]: API_PREVIOUS,
  [KEY_RIGHT]: API_NEXT,
  [KEY_UP]: API_FIRST,
  [KEY_DOWN]: API_LAST,
};

// Photo container
const photo = document.getElementById('photo');

// Photo metadata elements
let $ = document.getElementById.bind(document);

const metadata = {
  taken: $('md-taken'),
  width: $('md-width'),
  height: $('md-height'),
  md5: $('md-md5'),
};

const links = {
  new_tab: $('md-new-tab'),
  download: $('md-download'),
};

const exif = {
  camera: $('exif-camera'),
  lens: $('exif-lens'),
  shutter_speed: $('exif-shutter-speed'),
  aperture: $('exif-aperture'),
  iso_speed: $('exif-iso-speed'),
};

function navigate(url) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (!(request.readyState === 4 && request.status === 200)) {
      return;
    }

    let response = JSON.parse(request.responseText);

    // Image element
    let image = photo.children[0];

    photo.dataset.md5 = response.metadata.md5;
    image.src = response.image_url;

    Object.keys(metadata).forEach(function(key) {
      metadata[key].innerText = response.metadata[key];
    });

    Object.keys(links).forEach(function(key) {
      links[key].children[0].href = response.metadata[key];
    });

    Object.keys(exif).forEach(function(key) {
      exif[key].innerText = response.exif[key];
    });

    window.history.pushState('', '', response.url);
  };

  request.open('GET', url, true);
  request.send();
}

function query_string(params) {
  let escape = encodeURIComponent;
  let query = Object.keys(params)
    .map(k => escape(k) + '=' + escape(params[k]))
    .join('&');

  return '?' + query;
}

document.onkeydown = function(e) {
  let photo = document.getElementById('photo');

  let query = query_string({
    'path': photo.dataset.path,
    'md5': photo.dataset.md5,
  });

  let key = e.keyCode;

  switch (key) {
    case KEY_LEFT:
    case KEY_RIGHT:
    case KEY_UP:
    case KEY_DOWN:
      e.preventDefault();

      let base = KEY_MAPPING[key.toString()];
      return navigate(base + query);
  }
};
