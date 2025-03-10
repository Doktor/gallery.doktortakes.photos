<template>
  <li
    class="sidebar-list-item"
    :class="{ 'sidebar-list-item-marker': showMarker }"
  >
    <slot></slot>
  </li>
</template>

<script>
export default {
  props: {
    showMarker: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style lang="scss">
.sidebar-list-item {
  display: block;

  font-size: variables.$sidebar-font-size;
  font-weight: 400;
  line-height: 1;

  &.sidebar-list-item-marker::before {
    content: "-";
    color: variables.$text-color;
    font-size: 1rem;
    font-weight: 400;

    margin-right: 2px;
  }
}
</style>
