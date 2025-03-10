<template>
  <li class="sidebar-list-item">
    <slot></slot>
  </li>
</template>

<style lang="scss">
.sidebar-list-item {
  display: block;

  @include variables.sidebar-font();
}
</style>
