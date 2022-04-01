<template>
  <img
    v-if="hasThumbnail"
    :src="thumbnail"
    alt="Photo thumbnail"
  >
  <div v-else class="photo-placeholder">
    <PhotoPlaceholder/>
    <div class="photo-no-thumbnail-note">No thumbnail</div>
  </div>
</template>

<script>
  import PhotoPlaceholder from "./PhotoPlaceholder";


  export default {
    components: {
      PhotoPlaceholder,
    },

    computed: {
      hasThumbnail() {
        return this.photo.images.square?.url ?? false
      },
      thumbnail() {
        return this.isLoaded
          ? this.photo.images.square.url
          : this.placeholder
      },

    },

    props: {
      photo: {
        type: Object,
        required: true,
      },

      isLoaded: {
        type: Boolean,
        required: true,
      },
    },
  }
</script>
