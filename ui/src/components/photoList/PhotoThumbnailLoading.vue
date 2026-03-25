<template>
  <div class="photo-thumbnail-loading" title="Loading...">
    <PhotoPlaceholderImage />
    <div class="photo-thumbnail-loading-icon">
      <i class="fas fa-spin fa-spinner"></i>
    </div>
  </div>
</template>

<script>
import PhotoPlaceholderImage from "./PhotoPlaceholderImage";

export default {
  components: {
    PhotoPlaceholderImage,
  },
};
</script>

<style lang="scss">
@use "@/styles/variables";

.photo-thumbnail-loading {
  border: 1px solid variables.$background-color-2;
  position: relative;
}

.photo-thumbnail-loading-icon {
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
