<template>
  <div class="tiles">
    <slot></slot>
  </div>
</template>

<style lang="scss">
.tiles {
  display: grid;

  column-gap: variables.$item-spacing;
  row-gap: variables.$item-spacing;

  margin: variables.$item-spacing 0;
}
</style>
