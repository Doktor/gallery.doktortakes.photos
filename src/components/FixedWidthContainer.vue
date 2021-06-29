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
  },

  computed: {
    styles() {
      return {
        "max-width": `${this.width}px`,
      }
    },
  },
}
</script>

<style scoped>
.container-fixed-width {
  text-align: left;
  margin: 0 auto;
}
</style>
