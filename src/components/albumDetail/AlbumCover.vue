<template>
  <figure
      class="group-cover"
      :class="{'group-cover-no-image': album.cover === null}"
  >
    <img
        v-if="album.cover !== null"
        alt="Cover photo"
        :src="album.cover.thumbnail"
        :title="album.name"
    >
    <img
        v-else
        alt="Cover photo placeholder"
        :src="placeholder"
        :title="album.name"
    >

    <AlbumCoverOverlay/>
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

      placeholder() {
        return staticFiles.coverPlaceholder;
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
  }

  .group-cover-no-image {
    background-color: rgb(20, 20, 20);
    border: 1px solid rgb(40, 40, 40);
  }
</style>
