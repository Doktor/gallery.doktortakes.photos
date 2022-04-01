<template>
  <div
    :is="allowSelect ? 'div' : 'router-link'"
    :to="allowSelect ? null : photoLink"
  >
    <img
      v-if="hasThumbnail"
      :src="thumbnail"
      alt="Photo thumbnail"
    >
    <div v-else class="photo-placeholder">
      <PhotoPlaceholder/>
      <div class="photo-no-thumbnail-note">No thumbnail</div>
    </div>
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

      photoLink() {
        return {
          name: 'photo',
          params: {
            path: this.photo.path,
            md5: this.photo.md5,
          },
          query: {
            code: this.$route.query.code,
          },
        }
      },
    },

    props: {
      photo: {
        type: Object,
        required: true,
      },

      allowSelect: {
        type: Boolean,
        required: true,
      },

      isLoaded: {
        type: Boolean,
        required: true,
      },
    }
  }
</script>
