<template>
  <span class="font-awesome-circle-icon">
    <i :class="iconClass"></i>
  </span>
</template>

<script>
export default {
  name: "FontAwesomeCircleIcon",
  props: {
    iconClass: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss">
// Encloses a Font Awesome icon in a circle
.font-awesome-circle-icon {
  display: inline-flex;
  justify-content: center;
  align-items: center;

  color: variables.$background-color;
  background-color: variables.$text-color;

  // Background: circle
  width: variables.$sidebar-font-size;
  height: variables.$sidebar-font-size;
  border-radius: 100%;

  // Foreground: icon
  i {
    font-size: math.div(variables.$sidebar-font-size, 2);
  }
}
</style>
