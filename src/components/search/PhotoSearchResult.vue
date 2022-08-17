<template>
  <div class="photo-wrapper">
    <div class="photo">
      <a :href="photoLink">
        <PhotoThumbnail :isLoaded="isLoaded" :photo="photo" />
      </a>
    </div>
  </div>
</template>

<script>
import PhotoThumbnail from "@/components/photoList/PhotoThumbnail";

export default {
  components: { PhotoThumbnail },

  props: {
    photo: {
      type: Object,
      required: true,
    },
  },

  computed: {
    isLoaded() {
      return this.photo.isLoaded;
    },

    photoLink() {
      if (!this.isLoaded) {
        return null;
      }

      let route = this.$router.resolve({
        name: "photo",
        params: {
          path: this.photo.path,
          md5: this.photo.md5,
        },
      });

      return route.href;
    },
  },
};
</script>
