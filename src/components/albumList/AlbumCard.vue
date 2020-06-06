<template>
  <div
    class="album-wrapper"
    :class="{'hidden': !isSkeleton && !isVisible}"
  >
    <div class="album" :class="classes">
      <AlbumThumbnail v-if="!isSkeleton" v-bind="{album, route, isLoaded}"/>
      <AlbumSkeleton v-else/>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../../store";
  import AlbumSkeleton from "./AlbumSkeleton.vue";
  import AlbumThumbnail from "./AlbumThumbnail.vue";


  export default {
    components: {
      AlbumSkeleton,
      AlbumThumbnail,
    },

    computed: {
      classes() {
        return {
          'album-hidden': this.album.access_level > 0,
          'album-no-cover': this.album.cover === null,
        }
      },
    },

    props: {
      album: {
        type: Object,
        required: true,
      },

      route: {
        type: String,
        default: "album",
      },

      isLoaded: {
        type: Boolean,
        default: false,
      },
      isSkeleton: {
        type: Boolean,
        default: false,
      },
      isVisible: {
        type: Boolean,
        required: true,
      },
    }
  }
</script>
