export default function initPhotoSwipe() {
  const photoswipe = document.getElementById('pswp');

  const items = this.photos.map((photo) => {
    return {
      src: photo.image,
      w: photo.width,
      h: photo.height,
    }
  });

  this.$refs.viewer.addEventListener('click', (event) => {
    event.preventDefault();

    let options = {
      history: false,

      captionEl: false,
      shareEl: false,

      escKey: true,
      arrowKeys: true,

      index: this.photo.index,

      showHideOpacity: true,
      closeOnScroll: false,

      showAnimationDuration: 500,

      getThumbBoundsFn: () => {
        let item = this.$refs.image;
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
      // Swipe right
      if (startX < endX) {
        return this.$store.commit('setPhoto', this.photo.index - 1);
      }
      // Swipe left
      if (startX > endX) {
        return this.$store.commit('setPhoto', this.photo.index + 1);
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

  const leftArrow = document.querySelector('.pswp__button--arrow--left');
  leftArrow.addEventListener('click', () => this.previous());

  const rightArrow = document.querySelector('.pswp__button--arrow--right');
  rightArrow.addEventListener('click', () => this.next());
}
