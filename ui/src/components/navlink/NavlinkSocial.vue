<template>
  <div class="nav-item-social">
    <a
      class="nav-item-link nav-item-fa-wrapper"
      target="blank"
      rel="noopener noreferrer"
      v-bind="$attrs"
    >
      <slot></slot>
    </a>
  </div>
</template>

<script>
export default {
  name: "NavlinkSocial",
  inheritAttrs: false,
};
</script>

<style lang="scss" scoped>
.nav-item-social {
  display: inline-block;

  a {
    text-decoration: none !important;
  }
}

.nav-item-fa-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    text-decoration: none;
  }
}
</style>
