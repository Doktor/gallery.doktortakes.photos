<template>
  <div class="photo-wrapper">
    <div class="photo">
      <a @click.prevent="onClick" :href="photoLink">
        <img
          v-if="photo.square_thumbnail"
          :src="getThumbnail"
          alt="Photo thumbnail"
        />
        <PhotoPlaceholder v-else />
      </a>
    </div>
  </div>
</template>

<script>
import PhotoPlaceholder from "@/components/photoList/PhotoPlaceholder";

export default {
  components: { PhotoPlaceholder },
  computed: {
    getThumbnail() {
      return this.isLoaded ? this.photo.square_thumbnail : this.placeholder;
    },

    isLoaded() {
      return this.photo.path !== undefined;
    },

    photoLink() {
      let route;

      if (!this.isLoaded) {
        route = this.$router.resolve({ name: "albums" }).href;
      } else {
        route = this.$router.resolve({
          name: "photo",
          params: {
            path: this.photo.path,
            md5: this.photo.md5,
          },
        });
      }

      return route.href;
    },
  },

  methods: {
    onClick() {
      if (!this.isLoaded) {
        return;
      }

      return this.$router.push(this.photoLink);
    },
  },

  props: {
    photo: {
      type: Object,
      required: true,
    },
  },
};
</script>
