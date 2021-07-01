<template>
  <div class="photo-viewer">
    <div v-if="isDebug" class="crosshair" />
    <div class="photo-image-container">
      <img
        class="photo-image"
        ref="image"
        @click="navigate"
        :src="imageUrl"
        :style="imageStyles"
        alt=""
        title="Click to zoom"
      />
    </div>
  </div>
</template>

<script>
  function clamp(value, min, max) {
    if (min > max) {
      return (min + max) / 2;
    }

    return Math.min(Math.max(value, min), max);
  }

  export default {
    props: {
      count: {
        type: Number,
        required: true,
      },
      onClick: {
        type: Function,
        default: () => {},
      },
      photo: {
        type: Object,
        required: true,
      },
      useHistory: {
        type: Boolean,
        default: true,
      }
    },

    data() {
      return {
        scale: 1,
        translateX: 0,
        translateY: 0,

        maxScale: 2,

        transitionProperties: ['transform', 'left', 'top'],
        transitionTime: 0.6,
        transitionTimingFunction: 'ease',
      }
    },

    computed: {
      isDebug() {
        return !this.production
      },
      imageUrl() {
        if (this.isDebug && (this.$route.query?.test ?? false)) {
          return "https://upload.wikimedia.org/wikipedia/commons/a/aa/Philips_PM5544.svg";
        }

        return this.photo.image;
      },

      imageStyles() {
        return {
          transition: this.transitions,
          transform: `scale(${this.scale})`,
          left: `${this.translateX}px`,
          top: `${this.translateY}px`,
        }
      },
      transitions() {
        return this.transitionProperties.map(this.getTransition).join(', ');
      },

      image() {
        return this.$refs.image;
      },
      imageWidth() {
        return this.image.naturalWidth;
      },
      imageHeight() {
        return this.image.naturalHeight;
      },
      imageRatio() {
        return this.imageWidth / this.imageHeight;
      },

      viewportWidth() {
        return this.image?.offsetWidth ?? 0;
      },
      viewportHeight() {
        return this.image?.offsetHeight ?? 0;
      },
      viewportRatio() {
        return this.viewportWidth / this.viewportHeight;
      },
    },

    methods: {
      getTransition(name) {
        return `${name} ${this.transitionTime}s ${this.transitionTimingFunction}`;
      },

      navigate(event) {
        if (!this.zoomEnabled && !this.navigateInternal(event)) {
          return;
        }

        this.zoomEnabled = !this.zoomEnabled;

        if (!this.zoomEnabled) {
          this.scale = 1;
          this.translateX = 0;
          this.translateY = 0;
        }
      },

      // Returns true if navigation was successful, or false otherwise
      navigateInternal(event) {
        let scale = this.maxScale;

        // The click location on the image, relative to the top-left corner
        let clickX = event.offsetX;
        let clickY = event.offsetY;

        // Important: since the image element uses "object-fit: contain",
        // its bounding box is the same size as the viewport
        let imageDisplayWidth = this.viewportWidth;
        let imageDisplayHeight = this.viewportHeight;

        // Calculate the image's actual display size
        if (this.viewportRatio > this.imageRatio) {
          // The viewport is wider than the image
          imageDisplayWidth = this.imageWidth * this.viewportHeight / this.imageHeight;

          // Check if the click location is on the actual image
          let widthDiff = this.viewportWidth - imageDisplayWidth;
          let clickXFromEdge = Math.min(clickX, this.viewportWidth - clickX);

          if (clickXFromEdge <= widthDiff / 2) {
            return false;
          }
        }
        else {
          // The viewport is taller than the image
          imageDisplayHeight = this.imageHeight * this.viewportWidth / this.imageWidth;

          let heightDiff = this.viewportHeight - imageDisplayHeight;
          let clickYFromEdge = Math.min(clickY, this.viewportHeight - clickY);

          if (clickYFromEdge <= heightDiff / 2) {
            return false;
          }
        }

        // The center of the image
        let centerX = this.viewportWidth / 2;
        let centerY = this.viewportHeight / 2;

        let clickXDiff = clamp(
          centerX - clickX,
          0.5 / scale * this.viewportWidth - 0.5 * imageDisplayWidth,
          -0.5 / scale * this.viewportWidth + 0.5 * imageDisplayWidth
        );
        let clickYDiff = clamp(
          centerY - clickY,
          0.5 / scale * this.viewportHeight - 0.5 * imageDisplayHeight,
          -0.5 / scale * this.viewportHeight + 0.5 * imageDisplayHeight
        );

        this.scale = scale;
        this.translateX = clickXDiff * scale;
        this.translateY = clickYDiff * scale;
        return true;
      },

      first() {
        this.$store.commit(
          'setPhoto', {index: 0, history: this.useHistory});
      },
      previous() {
        this.$store.commit(
          'setPhoto', {index: this.photo.index - 1, history: this.useHistory});
      },
      next() {
        this.$store.commit(
          'setPhoto', {index: this.photo.index + 1, history: this.useHistory});
      },
      last() {
        this.$store.commit(
          'setPhoto', {index: this.count, history: this.useHistory});
      },
    },

    mounted() {
      document.addEventListener('keydown', (event) => {
        if (event.ctrlKey || event.metaKey) {
          return;
        }

        if (event.key.startsWith("Arrow")) {
          event.preventDefault();

          switch (event.key) {
            case "ArrowLeft":
              return this.previous();
            case "ArrowRight":
              return this.next();
            case "ArrowUp":
              return this.first();
            case "ArrowDown":
              return this.last();
          }
        }
      });
    },
  }
</script>

<style lang="scss" scoped>
  .photo-viewer {
    width: 100%;
    height: 100vh;
  }

  .photo-image-container {
    overflow: hidden;
    position: absolute;

    width: 100%;
    height: 100%;
  }

  .photo-image {
    display: block;
    overflow: hidden;
    position: absolute;

    width: 100%;
    height: 100%;

    object-fit: contain;
    transform-origin: center;
  }

  .crosshair {
    position: absolute;
    z-index: 1000;

    width: 100%;
    height: 100%;

    background:
      linear-gradient(red, red) no-repeat center / 2px 100%,
      linear-gradient(red, red) no-repeat center / 100% 2px;

    pointer-events: none;
  }
</style>
