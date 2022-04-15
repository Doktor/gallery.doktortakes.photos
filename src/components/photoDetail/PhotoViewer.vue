<template>
  <div>
    <div v-if="showCrosshair" class="crosshair"></div>
    <img
      class="photo-container"
      ref="container"
      @pointerdown.stop.prevent="pointerDown"
      @pointermove.stop.prevent="pointerMove"
      @pointerup.stop.prevent="pointerUp"
      @pointerleave.stop.prevent="pointerLeave"
      :src="src"
      :style="containerStyles"
      alt=""
      title="Click or tap to zoom"
    />
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
    },
  },

  data() {
    return {
      scale: 1,
      translateX: 0,
      translateY: 0,

      scaleLevels: [1, 2, 4],

      transitionProperties: ["transform", "left", "top"],
      transitionTime: 0.6,
      transitionTimingFunction: "ease",

      dragging: false,
      delayTranslateX: null,
      delayTranslateY: null,
      lastClientX: null,
      lastClientY: null,

      // Click/tap detection
      pointerStartX: null,
      pointerStartY: null,
      delta: 10,

      containerWidth: 0,
      containerHeight: 0,
    };
  },

  computed: {
    showCrosshair() {
      return this.$route.query?.crosshair ?? false;
    },

    src() {
      if (this.$route.query?.test ?? false) {
        return "https://upload.wikimedia.org/wikipedia/commons/a/aa/Philips_PM5544.svg";
      }

      return this.photo.images.display.url;
    },
    containerStyles() {
      let styles = {
        transition: this.transitions,
        transform: `scale(${this.scale})`,
        left: `${this.translateX}px`,
        top: `${this.translateY}px`,
      };

      if (this.scale > 1) {
        styles.touchAction = "none";
      }

      return styles;
    },
    transitions() {
      return this.transitionProperties.map(this.getTransition).join(", ");
    },

    imageWidth() {
      return this.photo.width;
    },
    imageHeight() {
      return this.photo.height;
    },
    imageRatio() {
      return this.imageWidth / this.imageHeight;
    },

    container() {
      return this.$refs.container;
    },
    containerRatio() {
      return this.containerWidth / this.containerHeight;
    },

    nextScale() {
      const index = this.scaleLevels.indexOf(this.scale);
      return this.scaleLevels[(index + 1) % this.scaleLevels.length];
    },
  },

  methods: {
    eventIsClickOrTap(event) {
      const diffX = Math.abs(this.pointerStartX - event.clientX);
      const diffY = Math.abs(this.pointerStartY - event.clientY);

      return diffX < this.delta && diffY < this.delta;
    },

    getTransition(name) {
      return `${name} ${this.transitionTime}s ${this.transitionTimingFunction}`;
    },

    pointerDown(event) {
      // Allow primary button only
      if (event.button !== 0) {
        return;
      }

      this.pointerStartX = event.clientX;
      this.pointerStartY = event.clientY;

      this.dragging = true;
      this.lastClientX = event.clientX;
      this.lastClientY = event.clientY;
    },
    pointerMove(event) {
      this.panImage(event);
    },
    pointerUp(event) {
      this.resetPointer();

      if (this.eventIsClickOrTap(event)) {
        this.scaleImage(event);
      }
    },
    pointerLeave(event) {
      this.resetPointer();
    },

    resetPointer() {
      this.dragging = false;

      if (this.delayTranslateX !== null) {
        this.translateX = this.delayTranslateX;
        this.translateY = this.delayTranslateY;

        this.delayTranslateX = null;
        this.delayTranslateY = null;
      }

      this.lastClientX = null;
      this.lastClientY = null;

      this.transitionProperties = ["transform", "left", "top"];
    },

    // Exits early if scaling is unsuccessful (if the pointer isn't on the actual image)
    scaleImage(event) {
      let scale = this.nextScale;

      // The pointer location on the container, relative to the top-left corner
      let pointerX = event.offsetX;
      let pointerY = event.offsetY;

      // Important: since the image element uses "object-fit: contain",
      // its bounding box is the same size as the container
      // Calculate the image's actual display size
      let imageDisplayWidth, imageDisplayHeight;

      if (this.containerRatio > this.imageRatio) {
        // The container is wider than the image
        imageDisplayWidth =
          (this.imageWidth * this.containerHeight) / this.imageHeight;
        imageDisplayHeight = this.containerHeight;

        // Check if the pointer location is on the actual image
        let widthDiff = this.containerWidth - imageDisplayWidth;
        let pointerXFromEdge = Math.min(
          pointerX,
          this.containerWidth - pointerX
        );

        if (pointerXFromEdge <= widthDiff / 2) {
          return;
        }
      } else {
        // The container is taller than the image
        imageDisplayWidth = this.containerWidth;
        imageDisplayHeight =
          (this.imageHeight * this.containerWidth) / this.imageWidth;

        let heightDiff = this.containerHeight - imageDisplayHeight;
        let pointerYFromEdge = Math.min(
          pointerY,
          this.containerHeight - pointerY
        );

        if (pointerYFromEdge <= heightDiff / 2) {
          return;
        }
      }

      // The center of the image
      let centerX = this.containerWidth / 2;
      let centerY = this.containerHeight / 2;

      let pointerXDiff = clamp(
        centerX - pointerX,
        centerX / scale - imageDisplayWidth / 2,
        -centerX / scale + imageDisplayWidth / 2
      );
      let pointerYDiff = clamp(
        centerY - pointerY,
        centerY / scale - imageDisplayHeight / 2,
        -centerY / scale + imageDisplayHeight / 2
      );

      this.scale = scale;
      this.translateX = pointerXDiff * scale;
      this.translateY = pointerYDiff * scale;
    },

    panImage(event) {
      if (!this.dragging) {
        return;
      }

      if (this.lastClientX === null || this.lastClientY === null) {
        return;
      }

      if (this.eventIsClickOrTap(event)) {
        return;
      }

      let scale = this.scale;

      let pointerX = event.clientX;
      let pointerY = event.clientY;

      let xDiff = pointerX - this.lastClientX;
      let yDiff = pointerY - this.lastClientY;

      if (scale === 1) {
        return;
      }

      // Calculate the image's actual display size
      let imageDisplayWidth, imageDisplayHeight;

      if (this.containerRatio > this.imageRatio) {
        imageDisplayWidth =
          (this.imageWidth * this.containerHeight) / this.imageHeight;
        imageDisplayHeight = this.containerHeight;
      } else {
        imageDisplayWidth = this.containerWidth;
        imageDisplayHeight =
          (this.imageHeight * this.containerWidth) / this.imageWidth;
      }

      let pointerXDiffUnclamped = (this.translateX + xDiff) / scale;
      let pointerYDiffUnclamped = (this.translateY + yDiff) / scale;

      let imageDisplayCenterX = imageDisplayWidth / 2;
      let imageDisplayCenterY = imageDisplayHeight / 2;

      // Allow the image to be dragged past the image bounds
      let pointerXDiffStretch = clamp(
        pointerXDiffUnclamped,
        -imageDisplayCenterX,
        imageDisplayCenterX
      );
      let pointerYDiffStretch = clamp(
        pointerYDiffUnclamped,
        -imageDisplayCenterY,
        imageDisplayCenterY
      );

      let centerX = this.containerWidth / 2;
      let centerY = this.containerHeight / 2;

      // If the image was dragged past the image bounds,
      // reset the image pan to these values when the pointer is released
      let pointerXDiff = clamp(
        pointerXDiffUnclamped,
        centerX / scale - imageDisplayCenterX,
        -centerX / scale + imageDisplayCenterX
      );
      let pointerYDiff = clamp(
        pointerYDiffUnclamped,
        centerY / scale - imageDisplayCenterY,
        -centerY / scale + imageDisplayCenterY
      );

      this.transitionProperties = ["transform"];

      this.translateX = pointerXDiffStretch * scale;
      this.translateY = pointerYDiffStretch * scale;

      this.delayTranslateX = pointerXDiff * scale;
      this.delayTranslateY = pointerYDiff * scale;

      this.lastClientX = pointerX;
      this.lastClientY = pointerY;

      return false;
    },

    first() {
      this.$emit("changePhoto", 0);
    },
    previous() {
      this.$emit("changePhoto", this.photo.index - 1);
    },
    next() {
      this.$emit("changePhoto", this.photo.index + 1);
    },
    last() {
      this.$emit("changePhoto", this.count);
    },

    calculateContainerSize() {
      this.containerWidth = this.container?.offsetWidth ?? 0;
      this.containerHeight = this.container?.offsetHeight ?? 0;
    },
  },

  mounted() {
    document.addEventListener("keydown", (event) => {
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

    this.calculateContainerSize();
  },
  created() {
    window.addEventListener("resize", this.calculateContainerSize);
  },
  unmounted() {
    window.removeEventListener("resize", this.calculateContainerSize);
  },
};
</script>

<style lang="scss" scoped>
.photo-container {
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

  background: linear-gradient(red, red) no-repeat center / 2px 100%,
    linear-gradient(red, red) no-repeat center / 100% 2px;

  pointer-events: none;
}
</style>
