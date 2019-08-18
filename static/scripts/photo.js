// API paths
const api = document.getElementById('api');

const API_GET_ALBUM_PHOTOS = api.dataset.apiGetAlbumPhotos;
const API_PASSWORD = api.dataset.password || '';


// Navigation
const settings = {
  // Index of the current image
  position: null,
  // Number of items in the filmstrip
  nFilmstripItems: 9,
  // 1/2 of the above (hardcoded)
  half: 4,
};


// Gallery elements
let $ = document.getElementById.bind(document);

const photoContainer = document.getElementById('photo');
const photoLink = photoContainer.querySelector('.photo-link');

const filmstrip = $('filmstrip-container');

const metadata = {
  index: $('md-index'),
  taken: $('md-taken'),
  width: $('md-width'),
  height: $('md-height'),
  md5: $('md-md5'),
};

const links = {
  image: $('md-new-tab'),
  download: $('md-download'),
  admin: $('md-admin'),
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
const photoswipeItems = [];


// Album items
const items = [];
const preloaded = [];

const elements = {
  static: document.querySelector('.photo-static'),
  landscape: document.querySelector('.photo-landscape'),
  portrait: document.querySelector('.photo-portrait'),
  previous: document.querySelector('.photo-previous'),
  next: document.querySelector('.photo-next'),
};

// Updates the primary photo
function loadPhoto(index, history = true) {
  if (settings.position === index) {
    return;
  }

  let itemsLength = items.length;

  // Loop to the other end at the start/end of the album
  if (index < 0) {
    index = itemsLength - 1;
  } else if (index > itemsLength - 1) {
    index = 0;
  }

  settings.position = index;

  // Get the new photo
  let item = items[index];

  // Update image
  photoLink.href = item.image;
  let isLandscape = item.width > item.height;

  if (isLandscape) {
    elements.landscape.src = item.image;
  } else {
    elements.portrait.src = item.image;
  }

  elements.landscape.classList.toggle('hidden', !isLandscape);
  elements.portrait.classList.toggle('hidden', isLandscape);

  // Update metadata
  ['index', 'md5', 'width', 'height'].forEach(function(key) {
    photoContainer.dataset[key] = item[key];
  });

  // Update primary metadata
  Object.keys(metadata).forEach(function(key) {
    metadata[key].innerText = item[key];
  });

  metadata.index.innerText = parseInt(item.index) + 1;

  // Update links
  Object.keys(links).forEach(function(key) {
    let el = links[key];

    if (el !== null) {
      el.querySelector('a').href = item[key];
    }
  });

  // Update EXIF
  Object.keys(exif).forEach(function(key) {
    exif[key].innerText = item.exif[key];
  });

  // Filmstrip
  let startIndex = 0, endIndex = 0;

  // Fewer items than filmstrip length
  if (itemsLength < settings.nFilmstripItems) {
    startIndex = 0;
    endIndex = itemsLength;
  }
  // Start
  else if (settings.position < settings.half) {
    startIndex = 0;
    endIndex = settings.nFilmstripItems;
  }
  // End
  else if (settings.position >= itemsLength - settings.half) {
    startIndex = itemsLength - settings.nFilmstripItems;
    endIndex = itemsLength;
  }
  // Middle
  else {
    startIndex = index - settings.half;
    endIndex = index + settings.half + 1;
  }

  Array.prototype.forEach.call(filmstrip.children, function(item, i) {
    item.classList.toggle('selected', i === index);
    item.classList.toggle('hidden', !(startIndex <= i && i < endIndex));
  });

  // Preload images

  // Adding "itemsLength" prevents negative indexes.
  let prevIndex = (settings.position - 1 + itemsLength) % itemsLength;
  let nextIndex = (settings.position + 1) % itemsLength;

  let prev = items[prevIndex];

  if (!prev.isPreloaded) {
    prev.isPreloaded = true;

    let prevImage = new Image();
    prevImage.src = items[prevIndex].image;
    preloaded.push(prevImage);
  }

  let next = items[nextIndex];
  if (!next.isPreloaded) {
    next.isPreloaded = true;

    let nextImage = new Image();
    nextImage.src = items[nextIndex].image;
    preloaded.push(nextImage);
  }

  // Browser history
  if (history) {
    let shortMD5 = item.md5.slice(0, 8);

    window.history.pushState('', shortMD5, item.url);

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
      if (item.md5 === api.dataset.md5) { thisIndex = i; }

      photoswipeItems.push({
        'src': item.image_url,
        'w': item.width,
        'h': item.height,
      })
    });

    response.photos.forEach(function(item) {
      // Container
      let div = document.createElement('div');
      div.classList.add('item');
      div.classList.add('hidden');

      // Image
      let image = document.createElement('img');
      image.src = item.square_thumbnail;
      image.addEventListener('click', () => loadPhoto(item.index));

      // Index
      let index = document.createElement('div');
      index.classList.add('index');
      index.innerText = parseInt(item.index) + 1;

      div.appendChild(image);
      div.appendChild(index);

      // Add to fragment
      filmstrip.appendChild(div);
    });

    loadPhotoSwipe();
    loadPhoto(thisIndex, false);
  }

  let params = {
    path: photoContainer.dataset.path,
    password: API_PASSWORD,
  };
  let url = API_GET_ALBUM_PHOTOS + queryString(params, true);

  sendRequest('GET', url, onSuccess, null);
}

function getActiveImageElement() {
  return elements.landscape.classList.contains('hidden') ? elements.portrait : elements.landscape;
}

// Loads the PhotoSwipe object
function loadPhotoSwipe() {
  photoLink.addEventListener('click', function(event) {
    event.preventDefault();

    let options = {
      history: false,

      captionEl: false,
      shareEl: false,

      escKey: true,
      arrowKeys: true,

      index: parseInt(photoContainer.dataset.index),

      showHideOpacity: true,
      closeOnScroll: false,

      showAnimationDuration: 500,

      getThumbBoundsFn: function() {
        let item = getActiveImageElement();
        let y = window.pageYOffset || document.documentElement.scrollTop;
        let rect = item.getBoundingClientRect();

        return {x: rect.left, y: rect.top + y, w: rect.width};
      },
    };

    const gallery = new PhotoSwipe(
      photoswipe, PhotoSwipeUI_Default, photoswipeItems, options);

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

    document.addEventListener('keydown', function(e) {
      switch (event.key) {
        case "ArrowUp":
          e.preventDefault();
          return gallery.goTo(0);
        case "ArrowDown":
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
  elements.static.classList.add('hidden');

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

  if (event.ctrlKey || event.metaKey) { return; }

  switch (key) {
    case KEY_A:
      window.location.href = photoContainer.dataset.albumUrl;
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
