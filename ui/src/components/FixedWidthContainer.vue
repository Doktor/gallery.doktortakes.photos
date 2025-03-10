<template>
  <div class="container-fixed-width" :style="styles">
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      default: 1000,
    },

    isCentered: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    styles() {
      return {
        "max-width": `${this.width}px`,
        "margin": this.isCentered ? "0 auto" : "0",
      };
    },
  },
};
</script>

<style scoped>
.container-fixed-width {
  text-align: left;
}
</style>
