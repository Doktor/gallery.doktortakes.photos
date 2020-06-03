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

    <AlbumCoverInset/>
  </figure>
</template>


<script>
  import {mapState} from 'vuex';
  import {staticFiles} from "../../store";
  import AlbumCoverInset from "./AlbumCoverInset.vue";

  export default {
    components: {
      AlbumCoverInset,
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
