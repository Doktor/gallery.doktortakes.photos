let $;


// Arrow keys
const KEY_LEFT = 37;
const KEY_UP = 38;
const KEY_RIGHT = 39;
const KEY_DOWN = 40;


// API paths
const api = document.getElementById('api');

const API_GET = api.dataset.apiGet;
const API_PREVIOUS = api.dataset.apiPrevious;
const API_NEXT = api.dataset.apiNext;
const API_FIRST = api.dataset.apiFirst;
const API_LAST = api.dataset.apiLast;
const API_GET_ALBUM_PHOTOS = api.dataset.apiGetAlbumPhotos;


// Shortcut key mapping
const KEY_MAPPING = {
  [KEY_LEFT]: API_PREVIOUS,
  [KEY_RIGHT]: API_NEXT,
  [KEY_UP]: API_FIRST,
  [KEY_DOWN]: API_LAST,
};


// Photo container
const photo = document.getElementById('photo');
const link = photo.children[0];
const image = link.children[0];


// Photo metadata elements
$ = document.getElementById.bind(document);

const metadata = {
  index: $('md-index'),
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


// Generates query strings
function query_string(params) {
  let escape = encodeURIComponent;
  let query = Object.keys(params)
    .map(k => escape(k) + '=' + escape(params[k]))
    .join('&');

  return '?' + query;
}

function get_photo_query_string() {
  return query_string({
    'path': photo.dataset.path,
    'md5': photo.dataset.md5,
  });
}


// Updates the primary photo
function load_photo(url) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    if (request.status !== 200) {
      return console.log(request.responseText);
    }

    let response = JSON.parse(request.responseText);

    ['index', 'md5', 'width', 'height'].forEach(function(key) {
      photo.dataset[key] = response.metadata[key];
    });

    link.href = response.image_url;
    image.src = response.image_url;

    Object.keys(metadata).forEach(function(key) {
      metadata[key].innerText = response.metadata[key];
    });

    metadata.index.innerText = parseInt(response.metadata.index, 10) + 1;

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


// Navigation
document.addEventListener('keydown', function(e) {
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
      return load_photo(base + query);
  }
});


// PhotoSwipe container
const photoswipe = document.getElementsByClassName('pswp')[0];

// Album items
const items = [];

// Loads photos from the API
function load_photos(url) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    if (request.status !== 200) {
      return console.log(request.responseText);
    }

    let response = JSON.parse(request.responseText);

    // Generate gallery items
    response.photos.forEach(function (item) {
      items.push({
        'src': item.image_url,
        'w': item.metadata.width,
        'h': item.metadata.height,
      })
    });

    load_photoswipe();
  };

  request.open('GET', url, true);
  request.send();
}

// Loads the PhotoSwipe object
function load_photoswipe() {
  link.addEventListener('click', function(event) {
    event.preventDefault();

    let options = {
      history: false,

      captionEl: false,
      shareEl: false,

      escKey: true,
      arrowKeys: true,

      index: parseInt(photo.dataset.index, 10),

      showHideOpacity: true,
      closeOnScroll: false,

      showAnimationDuration: 500,

      getThumbBoundsFn: function() {
        let item = image;
        let y = window.pageYOffset || document.documentElement.scrollTop;
        let rect = item.getBoundingClientRect();

        return {x: rect.left, y: rect.top + y, w: rect.width};
      },
    };

    const gallery = new PhotoSwipe(
      photoswipe, PhotoSwipeUI_Default, items, options);

    gallery.init();

    document.addEventListener('keydown', function(e) {
      let key = e.keyCode;

      switch (key) {
        case KEY_UP:
          e.preventDefault();
          return gallery.goTo(0);

        case KEY_DOWN:
          e.preventDefault();
          return gallery.goTo(gallery.items.length - 1);
      }
    });
  });
}

// Navigation arrows
$ = document.getElementsByClassName.bind(document);

const leftArrow = $('pswp__button--arrow--left')[0];
const rightArrow = $('pswp__button--arrow--right')[0];

leftArrow.addEventListener('click', function() {
  let query = get_photo_query_string();
  load_photo(API_PREVIOUS + query);
});

rightArrow.addEventListener('click', function() {
  let query = get_photo_query_string();
  load_photo(API_NEXT + query);
});


// Load the primary photo
document.addEventListener('DOMContentLoaded', function() {
  let query = get_photo_query_string();
  load_photo(API_GET + query);
});


// Load the rest of the album
document.addEventListener('DOMContentLoaded', function() {
  let query = query_string({'path': photo.dataset.path});
  load_photos(API_GET_ALBUM_PHOTOS + query);
});
