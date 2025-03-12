<template>
  <img
    v-if="thumbnail !== null"
    class="photo-thumbnail"
    :src="thumbnail"
    alt="Photo thumbnail"
  />
  <PhotoThumbnailPlaceholder v-else />
</template>

<script setup>
import { computed } from "vue";
import PhotoThumbnailPlaceholder from "./PhotoThumbnailPlaceholder";

const props = defineProps({
  photo: {
    type: Object,
    required: true,
  },
});

const thumbnail = computed(() => {
  return (
    props.photo.images?.mediumSquare?.url ??
    props.photo.images?.square?.url ??
    null
  );
});
</script>

<style lang="scss">
.photo-thumbnail {
  width: 100%;
}
</style>
