<template>
  <figure
    class="album-cover"
    :class="classes"
  >
    <AlbumCoverOverlay :isSkeleton="isSkeleton"/>
    <img
      v-if="!isSkeleton && album.cover !== null"
      class="album-cover-image"
      alt="Cover photo"
      :src="album.cover.thumbnail"
      :title="album.name"
    >
  </figure>
</template>


<script>
  import {mapState} from 'vuex';
  import {staticFiles} from "../../store";
  import AlbumCoverOverlay from "./AlbumCoverOverlay.vue";

  export default {
    components: {
      AlbumCoverOverlay,
    },

    computed: {
      ...mapState([
        'album',
      ]),

      classes() {
        return {
          'is-empty': !this.isSkeleton && this.album.cover === null,
          'is-skeleton': this.isSkeleton,
        }
      },

      placeholder() {
        return staticFiles.coverPlaceholder;
      },
    },

    props: {
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
      border: 1px solid rgb(40, 40, 40);
    }
  }

  .album-cover-image {
    position: absolute;
    z-index: 0;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;

    width: 100%;
    height: 100%;
    object-fit: cover;
  }
</style>
