<template>
  <figure
      class="group-cover"
      :class="classes"
  >
    <img
        v-if="!isSkeleton && album.cover !== null"
        alt="Cover photo"
        :src="album.cover.thumbnail"
        :title="album.name"
    >
    <AlbumCoverOverlay :isSkeleton="isSkeleton"/>
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
          'no-image': this.isSkeleton || this.album.cover === null,
          'skeleton': this.isSkeleton,
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
  .group-cover {
    width: 100%;
    height: 50vh;

    position: relative;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    &.no-image {
      height: unset;

      background-color: rgb(20, 20, 20);
      border: 1px solid rgb(40, 40, 40);
    }

    &.skeleton {
      height: 20vh;
    }
  }
</style>
