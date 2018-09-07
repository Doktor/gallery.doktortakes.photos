let $;

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

const filmstrip = $('filmstrip-container');

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


function get_photo_query_string() {
  return query_string({
    'path': photo.dataset.path,
    'md5': photo.dataset.md5,
  });
}


// Updates the primary photo
function load_photo(url, history = true) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    if (request.status !== 200) {
      return console.log(request.responseText);
    }

    let response = JSON.parse(request.responseText);

    // Load metadata
    ['index', 'md5', 'width', 'height'].forEach(function(key) {
      photo.dataset[key] = response.metadata[key];
    });

    link.href = response.image_url;
    image.src = response.image_url;

    Object.keys(metadata).forEach(function(key) {
      metadata[key].innerText = response.metadata[key];
    });

    metadata.index.innerText = parseInt(response.metadata.index) + 1;

    // Load links
    Object.keys(links).forEach(function(key) {
      links[key].children[0].href = response.metadata[key];
    });

    // Load EXIF
    Object.keys(exif).forEach(function(key) {
      exif[key].innerText = response.exif[key];
    });

    // Load the filmstrip
    filmstrip.innerHTML = '';
    let items = document.createDocumentFragment();

    response.filmstrip.forEach((item) => {
      let div = document.createElement('div');
      div.classList.add('item');

      // Mark the current item as selected
      if (item.md5 === photo.dataset.md5) {
        div.classList.add('selected');
      }

      // Image
      let image = document.createElement('img');
      image.src = item.url;

      image.addEventListener('click', () => {
        let qs = query_string({
          'path': photo.dataset.path,
          'md5': item.md5,
        });

        load_photo(API_GET + qs);
      });

      // Index
      let index = document.createElement('div');
      index.classList.add('index');
      index.innerText = parseInt(item.index) + 1;

      // Add to fragment
      div.appendChild(image);
      div.appendChild(index);
      items.appendChild(div);
    });

    filmstrip.append(items);

    if (history) {
      let shortMD5 = response.metadata.md5.slice(0, 7);

      window.history.pushState('', shortMD5, response.url);

      let title = document.title.split(' | ');
      title[0] = shortMD5;
      document.title = title.join(' | ');
    }
  };

  request.open('GET', url, true);
  request.send();
}


// Navigation
document.addEventListener('keyup', function(e) {
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
const photoswipe = document.getElementById('pswp');

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

    // Sync Photoswipe mouse and touch navigation with metadata

    // This is somewhat unwieldy. Photoswipe defines a minimum swipe/drag
    // distance to navigate to the next/previous photo. However, it doesn't
    // always work. Instead of relying on swipe distance, we wait for PS to
    // trigger the 'afterChange' event, and check the swipe direction.

    // https://github.com/dimsemenov/PhotoSwipe/blob/40a50b5aa6ccbe5b710911a0c7b0976eed1d168c/src/js/gestures.js#L7

    let startX = 0;
    let startY = 0;
    let endX = 0;
    let endY = 0;

    ['mousedown', 'touchstart'].map(function(e) {
      photoswipe.addEventListener(e, function(event) {
        if (e === 'touchstart') {
          event = event.changedTouches[0];
        }

        startX = event.screenX;
        startY = event.screenY;
      });
    });

    ['mouseup', 'touchend'].map(function(e) {
      photoswipe.addEventListener(e, function(event) {
        if (e === 'touchend') {
          event = event.changedTouches[0];
        }

        endX = event.screenX;
        endY = event.screenY;
      });
    });

    gallery.listen('afterChange', function() {
      let query = query_string({
        'path': photo.dataset.path,
        'md5': photo.dataset.md5,
      });

      // Swipe right
      if (startX < endX) {
        return load_photo(API_PREVIOUS + query);
      }
      // Swipe left
      if (startX > endX) {
        return load_photo(API_NEXT + query);
      }
    });

    document.addEventListener('keyup', function(e) {
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
  load_photo(API_GET + query, false);
});


// Load the rest of the album
document.addEventListener('DOMContentLoaded', function() {
  let query = query_string({'path': photo.dataset.path});
  load_photos(API_GET_ALBUM_PHOTOS + query);
});


document.addEventListener('keydown', function(event) {
  let key = event.keyCode;

  switch (key) {
    case KEY_A:
      window.location.href = photo.dataset.albumUrl;
      break;
    case KEY_D:
      window.location.href = links.download.children[0].href;
      break;
    case KEY_H:
      window.location.href = '/';
      break;
    case KEY_L:
      window.location.href = '/albums/';
      break;
  }
});
