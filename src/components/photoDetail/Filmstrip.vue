<template>
  <section>
    <div v-for="photo in photos" :class="classes(photo.index)">
      <img
        class="filmstrip-image"
        :src="photo.images.square.url"
        @click="onClick(photo.index)"
        :title="`${photo.index + 1} of ${photos.length}`"
      />
    </div>
  </section>
</template>

<script>
const settings = {
  items: 9,
  half: 4,
};

export default {
  computed: {
    routeAccessCode() {
      return this.$route.query.code || "";
    },
  },

  data() {
    return {
      start: 0,
      end: 0,
    };
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

      // Fewer items than filmstrip length
      if (length < settings.items) {
        start = 0;
        end = length;
      }
      // Start
      else if (this.position < settings.half) {
        start = 0;
        end = settings.items;
      }
      // End
      else if (this.position >= length - settings.half) {
        start = length - settings.items;
        end = length;
      }
      // Middle
      else {
        start = this.position - settings.half;
        end = this.position + settings.half + 1;
      }

      this.start = start;
      this.end = end;
    },
  },

  mounted() {
    this.updateRange();
  },

  props: {
    photos: {
      type: Array,
      required: true,
    },
    position: {
      type: Number,
      required: true,
    },

    useHistory: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style lang="scss">
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

  border: 1px solid $text-color;
  margin: 0 4px;

  cursor: pointer;
}
</style>
