<template>
  <div class="album-thumbnail-placeholder">
    <AlbumPlaceholder :title="album.name" />
    <div class="note album-no-cover-note">No cover</div>
  </div>
</template>

<script>
import AlbumPlaceholder from "./AlbumPlaceholderImage";

export default {
  components: {
    AlbumPlaceholder,
  },

  props: {
    album: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.album-thumbnail-placeholder {
  background: variables.$background-color-2;
  border: 1px solid variables.$background-color-2;
}
</style>
