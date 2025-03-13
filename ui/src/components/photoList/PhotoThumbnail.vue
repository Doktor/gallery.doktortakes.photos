<template>
  <img class="photo-thumbnail" :src="thumbnail" alt="Photo thumbnail" />
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  photo: {
    type: Object,
    required: true,
  },
});

const thumbnail = computed(() => {
  return props.photo.images.mediumSquare?.url ?? props.photo.images.square.url;
});
</script>

<style lang="scss">
.photo-thumbnail {
  width: 100%;
}
</style>
