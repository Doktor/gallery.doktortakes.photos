<template>
  <svg
    class="placeholder-image"
    :viewBox="`0 0 ${width} ${height}`"
    xmlns="http://www.w3.org/2000/svg"
  >
    <rect :width="width" :height="height" fill-opacity="0" />
  </svg>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      default: 1,
    },
    height: {
      type: Number,
      default: 1,
    },
  },
};
</script>

<style lang="scss" scoped>
.placeholder-image {
  display: block;
}
</style>
