<template>
  <div class="lazy-image" :class="{'lazy-image-loaded': loaded}">
    <div
      v-if="placeholder"
      ref="placeholder"
      class="lazy-image-placeholder"
      :style="{background}"
    >
      <img :src="placeholder" alt="" v-bind="$attrs" />
    </div>

    <img
      ref="image"
      :alt="$attrs.alt || ''"
      :src="placeholder"
      v-bind="$attrs"
    />
  </div>
</template>

<script>
export default {
  name: "LazyImage",

  inheritAttrs: false,

  data() {
    return {
      loaded: false,
    }
  },

  props: {
    src: {
      type: String,
      required: true,
    },
    background: String,
  },

  computed: {
    placeholder() {
      const {width, height} = this.$attrs;

      if (!width || !height) {
        return "";
      }

      const canvasWidth = 1;

      const canvas = document.createElement("canvas");
      canvas.width = canvasWidth;
      canvas.height = (height / width) * canvasWidth;

      const context = canvas.getContext("2d");
      context.fillStyle = "#606060";
      context.fillRect(0, 0, canvas.width, canvas.height);

      return canvas.toDataURL()
    },
  },

  mounted() {
    let timeout;

    const observer = new IntersectionObserver(([entry]) => {
      const image = this.$refs.image;
      const placeholder = this.$refs.placeholder;

      image.addEventListener('load', () => {
        delete image.onload;
        this.loaded = true;

        if (placeholder) {
          timeout = setTimeout(() => placeholder.remove(), 400)
        }
      });

      if (entry.isIntersecting) {
        image.src = this.src;
        observer.disconnect();
      }
    });

    observer.observe(this.$el);

    this.$once("hook:beforeDestroy", () => {
      observer.disconnect();

      if (timeout) {
        clearTimeout(timeout);
      }
    })
  },
}
</script>

<style lang="scss" scoped>
.lazy-image {
  display: block;
  position: relative;
}

.lazy-image-placeholder {
  position: absolute;
  overflow: hidden;

  img {
    transform: scale(1.05);
    filter: blur(10px);
  }
}

img {
  opacity: 0;
  transition: opacity 400ms ease-out;
}

.lazy-image-loaded img {
  opacity: 1;
}
</style>
