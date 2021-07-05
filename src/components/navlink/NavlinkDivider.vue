<template>
  <li class="nav-divider"></li>
</template>

<script>
export default {
  name: "NavlinkDivider",
};
</script>

<style lang="scss" scoped>
.nav-divider {
  @include secondary-headings-font();
  color: $text-color-2;
  font-style: normal !important;

  margin: 0 0.5rem !important;

  &::before {
    content: "\00b7"; // Center dot
  }
}
</style>
