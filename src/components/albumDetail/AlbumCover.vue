<template>
  <figure
      class="album-cover"
      :class="classes"
  >
    <AlbumCoverOverlay :album="album" :isSkeleton="isSkeleton" />
    <AlbumCoverImage v-if="!isSkeleton && album.cover !== null" />
  </figure>
</template>

<script>
import AlbumCoverImage from "./AlbumCoverImage";
import AlbumCoverOverlay from "./AlbumCoverOverlay";


export default {
  components: {
    AlbumCoverImage,
    AlbumCoverOverlay,
  },

  computed: {
    classes() {
      return {
        'is-empty': !this.isSkeleton && this.album.cover === null,
        'is-skeleton': this.isSkeleton,
      }
    },
  },

  props: {
    album: {
      type: Object,
      required: true,
    },

    isSkeleton: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.album-cover {
  position: relative;

  width: 100%;

  &.is-empty, &.is-skeleton {
    border: 1px solid $background-color-2;
  }
}
</style>
