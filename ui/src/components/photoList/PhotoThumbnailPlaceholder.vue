<template>
  <div class="photo-thumbnail-placeholder">
    <PhotoPlaceholderImage />
    <div class="photo-thumbnail-placeholder-note">No thumbnail</div>
  </div>
</template>

<script setup>
import PhotoPlaceholderImage from "./PhotoPlaceholderImage";
</script>

<style lang="scss">
.photo-thumbnail-placeholder {
  position: relative;
}

.photo-thumbnail-placeholder-note {
  position: absolute;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translateX(-50%) translateY(-50%);
}
</style>
