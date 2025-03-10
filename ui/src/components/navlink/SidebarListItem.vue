<template>
  <li class="sidebar-list-item">
    <slot></slot>
  </li>
</template>

<style lang="scss">
.sidebar-list-item {
  display: block;

  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1;

  &::before {
    content: "-";
    color: variables.$text-color;
    font-size: 1rem;
    font-weight: 400;

    margin-right: 2px;
  }
}
</style>
