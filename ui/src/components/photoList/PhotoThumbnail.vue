<template>
  <PhotoThumbnailLoading v-if="photo === undefined" />
  <img v-else class="photo-thumbnail" :src="thumbnail" alt="Photo thumbnail" />
</template>

<script setup>
import { computed } from "vue";
import PhotoThumbnailLoading from "@/components/photoList/PhotoThumbnailLoading.vue";

const props = defineProps({
  photo: {
    type: Object,
  },
});

const thumbnail = computed(() => {
  if (props.photo === undefined) {
    return null;
  }

  return props.photo.images.mediumSquare?.url ?? props.photo.images.square.url;
});
</script>

<style lang="scss">
.photo-thumbnail {
  width: 100%;
}
</style>
