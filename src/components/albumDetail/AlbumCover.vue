<template>
  <figure
    class="album-cover"
    :class="classes"
  >
    <AlbumCoverOverlay :isSkeleton="isSkeleton"/>
    <AlbumCoverImage v-if="!isSkeleton && album.cover !== null"/>
  </figure>
</template>

<script>
  import {mapState} from 'vuex';
  import {staticFiles} from "../../store";
  import AlbumCoverImage from "./AlbumCoverImage.vue";
  import AlbumCoverOverlay from "./AlbumCoverOverlay.vue";


  export default {
    components: {
      AlbumCoverImage,
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
</style>
