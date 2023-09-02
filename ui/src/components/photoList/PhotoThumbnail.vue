<template>
  <PhotoThumbnailLoading v-if="isLoading" />
  <img
    v-else-if="thumbnail !== null"
    class="photo-thumbnail"
    :src="thumbnail"
    alt="Photo thumbnail"
  />
  <PhotoThumbnailPlaceholder v-else />
</template>

<script>
import PhotoThumbnailLoading from "./PhotoThumbnailLoading";
import PhotoThumbnailPlaceholder from "./PhotoThumbnailPlaceholder";

export default {
  components: {
    PhotoThumbnailPlaceholder,
    PhotoThumbnailLoading,
  },

  props: {
    photo: {
      type: Object,
      required: true,
    },

    isLoading: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    thumbnail() {
      return (
        this.photo.images?.mediumSquare?.url ??
        this.photo.images?.square?.url ??
        null
      );
    },
  },
};
</script>

<style lang="scss">
.photo-thumbnail {
  width: 100%;
}
</style>
