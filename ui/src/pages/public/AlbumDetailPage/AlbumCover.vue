<template>
  <figure class="album-cover" :class="classes">
    <AlbumCoverOverlay
      :album="album"
      :count="count"
      :isSkeleton="isSkeleton"
      :showManage="showManage"
    />
    <AlbumCoverImage
      v-if="!isSkeleton && album.cover !== null"
      :album="album"
    />
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
        "is-empty": !this.isSkeleton && this.album.cover === null,
        "is-skeleton": this.isSkeleton,
      };
    },
  },

  props: {
    album: {
      type: Object,
      required: true,
    },
    count: {
      type: Number,
      required: true,
    },
    isSkeleton: {
      type: Boolean,
      default: false,
    },
    showManage: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.album-cover {
  position: relative;

  width: 100%;

  &.is-empty,
  &.is-skeleton {
    border: 1px solid variables.$background-color-2;
  }
}
</style>
