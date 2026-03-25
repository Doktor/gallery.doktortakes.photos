<template>
  <section>
    <div v-for="photo in photos" :class="classes(photo.index)">
      <img
        class="filmstrip-image"
        :src="photo.images.extraSmallSquare?.url ?? photo.images.square.url"
        @click="onClick(photo.index)"
        :title="`${photo.index + 1} of ${photos.length}`"
      />
    </div>
  </section>
</template>

<script>
export default {
  props: {
    photos: {
      type: Array,
      required: true,
    },
    position: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      start: 0,
      end: 0,
    };
  },

  computed: {
    count() {
      return 7;
    },
  },

  methods: {
    classes(index) {
      this.updateRange();

      return {
        "filmstrip-item": true,
        "hidden": !(this.start <= index && index < this.end),
        "selected": this.position === index,
      };
    },

    onClick(index) {
      this.$emit("changePhoto", index);
    },

    updateRange() {
      let start;
      let end;

      let length = this.photos.length;
      let half = Math.trunc(this.count / 2);

      // Fewer items than filmstrip length
      if (length < this.count) {
        start = 0;
        end = length;
      }
      // Start
      else if (this.position < half) {
        start = 0;
        end = this.count;
      }
      // End
      else if (this.position >= length - half) {
        start = length - this.count;
        end = length;
      }
      // Middle
      else {
        start = this.position - half;
        end = this.position + half + 1;
      }

      this.start = start;
      this.end = end;
    },
  },

  mounted() {
    this.updateRange();
  },
};
</script>

<style lang="scss">
@use "@/styles/variables";

$fadeTime: 0.2s;

.filmstrip-item {
  $step: 0.35;

  display: inline-block;

  .filmstrip-image {
    opacity: 1 - $step * 2;
  }

  &:hover .filmstrip-image {
    opacity: 1 - $step;
  }

  .filmstrip-image,
  &:hover .filmstrip-image {
    transition: opacity $fadeTime ease-in-out;
  }

  &.selected .filmstrip-image,
  &.selected:hover .filmstrip-image {
    opacity: 1;
  }
}

.filmstrip-image {
  display: block;
  width: 50px;
  height: 50px;

  border: 1px solid variables.$text-color;
  margin: 0 4px;

  cursor: pointer;
}
</style>
