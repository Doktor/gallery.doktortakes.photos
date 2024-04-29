<template>
  <div class="album-cover-image" :style="styles"></div>
</template>

<script>
export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
  },

  computed: {
    styles() {
      return {
        backgroundImage: `url(${this.album.cover.thumbnail.url})`,
      };
    },
  },
};
</script>

<style lang="scss" scoped>
.album-cover-image {
  background: no-repeat 50% math.div(100%, 3);
  background-size: cover;

  &,
  &::after {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }

  &::after {
    content: "";

    backdrop-filter: blur(8px);
    pointer-events: none;
  }
}
</style>
