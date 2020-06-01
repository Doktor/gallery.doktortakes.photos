<template>
  <section class="photo">
    <div class="photo-image-container" @click="onClick">
      <img
          class="photo-image photo-landscape"
          :class="{'hidden': isPortrait}"
          :src="photo.image"
          alt="Container for landscape photos"
          title="Click to zoom"
      >
      <img
          class="photo-image photo-portrait"
          :class="{'hidden': isLandscape}"
          :src="photo.image"
          alt="Container for portrait photos"
          title="Click to zoom"
      >
    </div>
  </section>
</template>

<script>
  export default {
    computed: {
      isLandscape() {
        return this.photo.width >= this.photo.height;
      },

      isPortrait() {
        return !this.isLandscape;
      },
    },

    methods: {
      first() {
        this.$store.commit(
          'setPhoto', {index: 0, history: this.useHistory});
      },
      previous() {
        this.$store.commit(
          'setPhoto', {index: this.photo.index - 1, history: this.useHistory});
      },
      next() {
        this.$store.commit(
          'setPhoto', {index: this.photo.index + 1, history: this.useHistory});
      },
      last() {
        this.$store.commit(
          'setPhoto', {index: this.count, history: this.useHistory});
      },
    },

    mounted() {
      document.addEventListener('keydown', (event) => {
        if (event.ctrlKey || event.metaKey) {
          return;
        }

        if (event.key.startsWith("Arrow")) {
          event.preventDefault();

          switch (event.key) {
            case "ArrowLeft":
              return this.previous();
            case "ArrowRight":
              return this.next();
            case "ArrowUp":
              return this.first();
            case "ArrowDown":
              return this.last();
          }
        }
      });
    },

    props: {
      count: {
        type: Number,
        required: true,
      },
      onClick: {
        type: Function,
        default: () => {},
      },
      photo: {
        type: Object,
        required: true,
      },
      useHistory: {
        type: Boolean,
        default: true,
      }
    },
  }
</script>

<style lang="scss" scoped>
  .photo {
    display: flex;
    justify-content: center;
    align-items: center;

    margin: 0;
    width: 100%;

    @media (min-width: 1201px) {
      height: 100vh;
    }
  }

  .photo-image-container {
    cursor: pointer;
  }

  .photo-image {
    max-width: 100%;
    max-height: 100vh;
  }
</style>
