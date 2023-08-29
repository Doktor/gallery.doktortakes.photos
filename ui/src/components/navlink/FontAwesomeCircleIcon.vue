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
  display: flex;
  justify-content: center;
  align-items: center;

  // Background: circle
  width: 24px;
  height: 24px;
  border-radius: 100%;

  color: $background-color;
  background-color: $text-color;

  // Foreground: icon
  i {
    font-size: 50%;
  }
}
</style>
