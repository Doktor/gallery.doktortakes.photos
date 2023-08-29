<template>
  <li class="nav-item nav-divider"></li>
</template>

<script>
export default {
  name: "NavlinkDivider",
};
</script>

<style lang="scss" scoped>
.nav-divider {
  display: none;

  @include secondary-headings-font();
  color: $text-color-2;
  font-style: normal;

  margin: 0 math.div($nav-item-spacing, 3);
  margin-bottom: 1rem;

  &::before {
    content: "\00b7"; // Center dot
  }

  @media (min-width: 901px) {
    display: block;
  }
}
</style>
