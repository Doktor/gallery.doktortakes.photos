<template>
  <div class="album-thumbnail-loading" title="Loading...">
    <AlbumPlaceholderImage />
    <div class="album-thumbnail-loading-note">
      <i class="fas fa-spin fa-spinner"></i>
    </div>
  </div>
</template>

<script>
import AlbumPlaceholderImage from "./AlbumPlaceholderImage";

export default {
  components: {
    AlbumPlaceholderImage,
  },
};
</script>

<style lang="scss" scoped>
@use "@/styles/variables";

.album-thumbnail-loading {
  border: 1px solid variables.$background-color-2;
  position: relative;
}

.album-thumbnail-loading-note {
  position: absolute;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translateX(-50%) translateY(-50%);

  i {
    color: variables.$text-color-2;
  }
}
</style>
