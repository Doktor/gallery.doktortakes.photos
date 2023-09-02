<template>
  <FadeTransition appear :duration="1000" mode="in-out">
    <div class="hero-photo" :key="photo.image" :style="heroPhotoStyles">
      <img
        class="hero-photo-loader"
        :src="photo.image"
        @load.once="onInitialImageLoad"
        alt=""
      />
    </div>
  </FadeTransition>
</template>

<script>
import FadeTransition from "@/transitions/FadeTransition.vue";

export default {
  components: {
    FadeTransition,
  },

  props: {
    photo: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      initialImageLoaded: false,
    };
  },

  computed: {
    heroPhotoStyles() {
      let styles = {
        backgroundImage: `url(${this.photo.image})`,
        backgroundPositionX: this.photo.x_position ?? "center",
      };

      if (!this.initialImageLoaded) {
        styles.visibility = "hidden";
        styles.opacity = 0;
      }

      return styles;
    },
  },

  methods: {
    onInitialImageLoad() {
      this.initialImageLoaded = true;
    },
  },
};
</script>

<style scoped>
.hero-photo {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: -1;

  transform: scale(1.2);

  background-repeat: no-repeat;
  background-position: center center;
  background-attachment: fixed;
  background-size: cover;

  cursor: pointer;
}

.hero-photo-loader {
  display: none;
}
</style>
