<template>
  <AlbumTileWrapper v-show="isVisible">
    <div class="album" :class="classes">
      <component
        :is="isLoading ? 'div' : 'router-link'"
        :to="isLoading ? null : albumLink"
      >
        <AlbumThumbnail :isLoading="isLoading" :album="album" />
      </component>
    </div>
  </AlbumTileWrapper>
</template>

<script>
import AlbumThumbnail from "./AlbumThumbnail.vue";
import AlbumTileWrapper from "./AlbumTileWrapper.vue";

export default {
  components: {
    AlbumTileWrapper,
    AlbumThumbnail,
  },

  computed: {
    classes() {
      return {
        "album-hidden": this.album.access_level > 0,
        "album-no-cover": this.album.cover === null,
      };
    },

    albumLink() {
      return {
        name: this.routeName,
        params: {
          path: this.album.pathSplit,
        },
      };
    },
  },

  props: {
    album: {
      type: Object,
      required: true,
    },

    routeName: {
      type: String,
      default: "album",
    },

    isLoading: {
      type: Boolean,
      required: true,
    },
    isVisible: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.album {
  position: relative;
}
</style>
