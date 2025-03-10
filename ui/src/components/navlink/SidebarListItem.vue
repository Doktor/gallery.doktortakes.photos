<template>
  <li class="sidebar-list-item">
    <slot></slot>
  </li>
</template>

<style lang="scss">
.sidebar-list-item {
  display: block;

  font-size: variables.$sidebar-font-size;
  font-weight: 400;
  line-height: 1;
}
</style>
