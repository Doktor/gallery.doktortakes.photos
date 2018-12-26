let $;


// API paths
const api = document.getElementById('api');

const API_GET_ALBUM_PHOTOS = api.dataset.apiGetAlbumPhotos;
const API_PASSWORD = api.dataset.password || '';


// Photo container
const photo = document.getElementById('photo');
const link = photo.children[0];
const image = link.children[0];


// Navigation
const settings = {
  position: null,
  items: 9,
  half: 4,
};


// Gallery elements
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


// PhotoSwipe
const photoswipe = document.getElementById('pswp');
const psItems = [];


// Album items
const items = [];



// Updates the primary photo
function loadPhoto(index, history = true) {
  if (settings.position === index) { return; }

  // Loop around at the start/end of the album
  if (index < 0) { index = items.length - 1; }
  else if (index > items.length - 1) { index = 0; }

  let response = items[index];
  settings.position = index;

  // Metadata
  ['index', 'md5', 'width', 'height'].forEach(function(key) {
    photo.dataset[key] = response.metadata[key];
  });

  link.href = response.image_url;
  image.src = response.image_url;

  Object.keys(metadata).forEach(function(key) {
    metadata[key].innerText = response.metadata[key];
  });

  metadata.index.innerText = parseInt(response.metadata.index) + 1;

  // Links
  Object.keys(links).forEach(function(key) {
    links[key].children[0].href = response.metadata[key];
  });

  // EXIF
  Object.keys(exif).forEach(function(key) {
    exif[key].innerText = response.exif[key];
  });

  // Filmstrip
  let start = 0, end = 0;

  // Fewer items than filmstrip length
  if (items.length < settings.items) {
    start = 0;
    end = items.length;
  }
  // Beginning of the filmstrip
  else if (settings.position < (settings.half)) {
    start = 0;
    end = settings.items;
  }
  // End of the filmstrip
  else if (settings.position >= (items.length - settings.half)) {
    start = items.length - settings.items;
    end = items.length;
  }
  // Everything else
  else {
    start = index - settings.half;
    end = index + settings.half + 1;
  }

  Array.prototype.forEach.call(filmstrip.children, function(item, i) {
    item.classList.toggle('selected', i === index);
    item.classList.toggle('hidden', !(start <= i && i < end));
  });

  // Browser history
  if (history) {
    let shortMD5 = response.metadata.md5.slice(0, 8);

    window.history.pushState('', shortMD5, response.url);

    let title = document.title.split(' | ');
    title[0] = shortMD5;
    document.title = title.join(' | ');
  }
}

// Loads photos from the API
function loadPhotos() {
  function onSuccess(response) {
    let thisIndex = 0;

    // Generate gallery items
    response.photos.forEach(function(item, i) {
      items.push(item);

      // Get index of this item
      if (item.metadata.md5 === api.dataset.md5) { thisIndex = i; }

      psItems.push({
        'src': item.image_url,
        'w': item.metadata.width,
        'h': item.metadata.height,
      })
    });

    response.photos.forEach(function(item) {
      // Container
      let div = document.createElement('div');
      div.classList.add('item');
      div.classList.add('hidden');

      // Image
      let image = document.createElement('img');
      image.src = item.square_thumbnail_url;
      image.addEventListener('click', () => loadPhoto(item.metadata.index));

      // Index
      let index = document.createElement('div');
      index.classList.add('index');
      index.innerText = parseInt(item.metadata.index) + 1;

      div.appendChild(image);
      div.appendChild(index);

      // Add to fragment
      filmstrip.appendChild(div);
    });

    loadPhotoSwipe();
    loadPhoto(thisIndex, false);
  }

  let params = {
    path: photo.dataset.path,
    password: API_PASSWORD,
  };
  let url = API_GET_ALBUM_PHOTOS + queryString(params, true);

  sendRequest('GET', url, onSuccess, null);
}

// Loads the PhotoSwipe object
function loadPhotoSwipe() {
  link.addEventListener('click', function(event) {
    event.preventDefault();

    let options = {
      history: false,

      captionEl: false,
      shareEl: false,

      escKey: true,
      arrowKeys: true,

      index: parseInt(photo.dataset.index),

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
      photoswipe, PhotoSwipeUI_Default, psItems, options);

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
      // Swipe right
      if (startX < endX) {
        return loadPhoto(settings.position - 1);
      }
      // Swipe left
      if (startX > endX) {
        return loadPhoto(settings.position + 1);
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

  // Mouse navigation
  $ = document.getElementsByClassName.bind(document);

  const leftArrow = $('pswp__button--arrow--left')[0];
  const rightArrow = $('pswp__button--arrow--right')[0];

  leftArrow.addEventListener('click', () => loadPhoto(settings.position - 1));
  rightArrow.addEventListener('click', () => loadPhoto(settings.position + 1));

}

// Load the album
document.addEventListener('DOMContentLoaded', () => {
  loadPhotos();

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    let key = e.keyCode;

    switch (key) {
      case KEY_LEFT:
        e.preventDefault();
        return loadPhoto(settings.position - 1);
      case KEY_RIGHT:
        e.preventDefault();
        return loadPhoto(settings.position + 1);
      case KEY_UP:
        e.preventDefault();
        return loadPhoto(0);
      case KEY_DOWN:
        e.preventDefault();
        return loadPhoto(items.length - 1);
    }
  });
});

// Keyboard shortcuts
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
